"""Generate six standalone glTF binary wine-bottle models from catalog photography.

The photographs are frontal views; bottle shape, side and rear surfaces are
reconstructed, while the front label/capsule artwork is sampled from the photos.
"""

from __future__ import annotations

import io
import json
import math
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "models"

WINES = [
    ("kisi-amber-2023", "kisi-original.png", "amber", "gold"),
    ("khikhvi-reserve-2022", "khikhvi-original.png", "amber", "gold"),
    ("rkatsiteli-qvevri-2023", "rkatsiteli-original.png", "amber", "gold"),
    ("kindzmarauli-2023", "kindzmarauli-original.png", "red", "burgundy"),
    ("mukuzani-reserve-2021", "mukuzani-original.png", "red", "black"),
    ("saperavi-qvevri-2022", "saperavi-original.png", "red", "burgundy"),
]


class Model:
    def __init__(self, name: str):
        self.bin = bytearray()
        self.views = []
        self.accessors = []
        self.meshes = []
        self.nodes = []
        self.materials = []
        self.images = []
        self.textures = []
        self.name = name

    def buffer_view(self, data: bytes, target=None):
        while len(self.bin) % 4:
            self.bin.append(0)
        offset = len(self.bin)
        self.bin.extend(data)
        view = {"buffer": 0, "byteOffset": offset, "byteLength": len(data)}
        if target:
            view["target"] = target
        self.views.append(view)
        return len(self.views) - 1

    def accessor(self, array, component_type, shape, target):
        a = np.asarray(array)
        if component_type == 5126:
            a = a.astype('<f4')
        elif component_type == 5123:
            a = a.astype('<u2')
        elif component_type == 5125:
            a = a.astype('<u4')
        else:
            raise ValueError(component_type)
        vi = self.buffer_view(a.tobytes(), target)
        obj = {"bufferView": vi, "componentType": component_type,
               "count": len(a), "type": shape}
        if shape == 'VEC3':
            obj["min"] = a.min(axis=0).tolist()
            obj["max"] = a.max(axis=0).tolist()
        self.accessors.append(obj)
        return len(self.accessors) - 1

    def add_texture(self, photo: Image.Image, name: str):
        stream = io.BytesIO()
        photo.save(stream, 'JPEG', quality=92, subsampling=0, optimize=True)
        view = self.buffer_view(stream.getvalue())
        self.images.append({"name": name, "mimeType": "image/jpeg", "bufferView": view})
        self.textures.append({"name": name, "source": len(self.images) - 1, "sampler": 0})
        return len(self.textures) - 1

    def material(self, name, color, roughness, metallic=0.0, texture=None, gloss=None):
        pbr = {"baseColorFactor": [*color, 1.0], "roughnessFactor": roughness,
               "metallicFactor": metallic}
        if texture is not None:
            pbr["baseColorTexture"] = {"index": texture}
        obj = {"name": name, "pbrMetallicRoughness": pbr, "doubleSided": False}
        if gloss is not None:
            obj["extras"] = {"finish": gloss}
        self.materials.append(obj)
        return len(self.materials) - 1

    def add_mesh(self, name, positions, normals, texcoords, faces, material):
        p = self.accessor(positions, 5126, 'VEC3', 34962)
        n = self.accessor(normals, 5126, 'VEC3', 34962)
        t = self.accessor(texcoords, 5126, 'VEC2', 34962)
        indices = np.asarray(faces, dtype=np.uint16).reshape(-1)
        f = self.accessor(indices, 5123, 'SCALAR', 34963)
        self.meshes.append({"name": name, "primitives": [{"attributes": {
            "POSITION": p, "NORMAL": n, "TEXCOORD_0": t}, "indices": f,
            "material": material, "mode": 4}]})
        self.nodes.append({"name": name, "mesh": len(self.meshes) - 1})

    def write(self, path):
        gltf = {"asset": {"version": "2.0", "generator": "BEQSON Wine Model Studio"},
                "scene": 0, "scenes": [{"nodes": list(range(len(self.nodes)))}],
                "nodes": self.nodes, "meshes": self.meshes,
                "materials": self.materials, "images": self.images,
                "textures": self.textures,
                "samplers": [{"magFilter": 9729, "minFilter": 9987,
                              "wrapS": 33071, "wrapT": 33071}],
                "bufferViews": self.views, "accessors": self.accessors,
                "buffers": [{"byteLength": len(self.bin)}],
                "extras": {"source": "Kakheti Wine House concept photography",
                           "accuracy": "3D shape reconstructed; genuine front label image"}}
        json_data = json.dumps(gltf, ensure_ascii=False, separators=(',', ':')).encode()
        json_data += b' ' * ((-len(json_data)) % 4)
        bin_data = bytes(self.bin) + b'\0' * ((-len(self.bin)) % 4)
        length = 12 + 8 + len(json_data) + 8 + len(bin_data)
        with path.open('wb') as out:
            out.write(struct.pack('<III', 0x46546C67, 2, length))
            out.write(struct.pack('<I4s', len(json_data), b'JSON'))
            out.write(json_data)
            out.write(struct.pack('<I4s', len(bin_data), b'BIN\0'))
            out.write(bin_data)


def revolved(profile, divisions=96, theta_min=-math.pi, theta_max=math.pi,
             uv_mode="circumference"):
    points, normals, uvs, faces = [], [], [], []
    for j, (height, radius) in enumerate(profile):
        prev = profile[max(0, j-1)]
        nex = profile[min(j+1, len(profile)-1)]
        rise = nex[0] - prev[0]
        radial_slope = (nex[1] - prev[1]) / (rise or 1)
        for i in range(divisions + 1):
            u = i / divisions
            angle = theta_min + (theta_max - theta_min) * u
            sine, cosine = math.sin(angle), math.cos(angle)
            normal = np.array([sine, -radial_slope, cosine], dtype=np.float64)
            normal /= np.linalg.norm(normal)
            points.append((radius * sine, height, radius * cosine))
            normals.append(normal.tolist())
            if uv_mode == 'projected':
                u = (sine - math.sin(theta_min)) / (
                    math.sin(theta_max) - math.sin(theta_min)) if theta_min < 0 < theta_max else u
            uvs.append((u, 1 - j / (len(profile) - 1)))
    for j in range(len(profile) - 1):
        for i in range(divisions):
            a, b = j*(divisions+1)+i, (j+1)*(divisions+1)+i
            faces += [(a, a+1, b), (a+1, b+1, b)]
    return points, normals, uvs, faces


def label_surface(y_bottom, y_top, radius, arc=1.47, divisions=100, rows=32):
    """Patch with photo-projected UVs so frontal lettering stays proportionate."""
    points, normals, uvs, faces = [], [], [], []
    bound = math.sin(arc)
    for j in range(rows+1):
        t = j/rows
        y = y_bottom + (y_top-y_bottom)*t
        for i in range(divisions+1):
            theta = -arc + 2*arc*(i/divisions)
            sine, cosine = math.sin(theta), math.cos(theta)
            points.append((radius*sine,y,radius*cosine))
            normals.append((sine,0,cosine))
            uvs.append(((sine+bound)/(2*bound),1-t))
    for j in range(rows):
        for i in range(divisions):
            a = j*(divisions+1)+i
            b = (j+1)*(divisions+1)+i
            faces += [(a,a+1,b),(a+1,b+1,b)]
    return points,normals,uvs,faces


def crop_art(photo, rect, size):
    region = photo.crop(rect).resize(size, Image.Resampling.LANCZOS)
    return ImageEnhance.Contrast(region).enhance(1.02)


def build(filename, source, tone, foil):
    photo = Image.open(ROOT / source).convert('RGB')
    if photo.size != (1122, 1402):
        raise ValueError(f'Unexpected crop calibration for {source}: {photo.size}')

    model = Model(filename)
    label_art = crop_art(photo, (404, 598, 716, 1186), (512, 966))
    cap_art = crop_art(photo, (494, 92, 628, 275), (256, 350))
    front = model.add_texture(label_art, "Original front label")
    cap = model.add_texture(cap_art, "Original capsule emblem")
    label_art.save(OUTPUT / (filename + '-label.webp'), 'WEBP', quality=88, method=6)
    cap_art.save(OUTPUT / (filename + '-cap.webp'), 'WEBP', quality=88, method=6)

    glass = ((.37,.16,.052) if tone == 'amber' else (.075,.024,.036))
    foil_color = {'gold':(.60,.34,.11), 'burgundy':(.28,.046,.09), 'black':(.055,.055,.052)}[foil]
    glass_mat = model.material('Thick '+tone+' wine glass', glass, 0.13, 0.08, gloss='polished')
    label_mat = model.material('Authentic photographed front label', (1,1,1), 0.82, texture=front)
    foil_mat = model.material('Metallic '+foil+' capsule', foil_color, 0.28, 0.45)
    cap_mat = model.material('Original embossed capsule print', (1,1,1), 0.6, .05, texture=cap)
    punt_mat = model.material('Recessed bottle base',tuple(x*.65 for x in glass), .26, .05)

    profile = [
        (.001,.028),(.002,.033),(.004,.036),(.007,.038),(.013,.0385),
        (.035,.0385),(.062,.0385),(.132,.0385),(.177,.0385),(.196,.0385),
        (.205,.0383),(.210,.0377),(.215,.0360),(.221,.0324),(.227,.0280),
        (.234,.0226),(.240,.0182),(.246,.0160),(.251,.0153),(.260,.0153),
        (.283,.0153),(.302,.0153),(.308,.0155),
    ]
    model.add_mesh('Sculpted glass bottle', *revolved(profile), glass_mat)
    model.add_mesh('Gently curved photographed paper label',
                   *label_surface(.0415,.1755,.03905), label_mat)

    model.add_mesh('Foil capsule', *revolved([
        (.251,.01558),(.255,.0158),(.258,.0159),(.292,.0159),
        (.298,.0163),(.302,.0163),(.304,.0155),(.308,.0155),(.310,.0136),
    ]), foil_mat)
    model.add_mesh('Original capsule emblem',
                   *label_surface(.257,.293,.01616,arc=1.42,rows=16), cap_mat)
    model.add_mesh('Capsule lip', *revolved([
        (.300,.0154),(.302,.0171),(.307,.0171),(.309,.0165),(.310,.0138)
    ]), foil_mat)
    model.add_mesh('Heavy glass heel', *revolved([
        (.000,.0265),(.0008,.0315),(.003,.036),(.006,.0382)
    ]), punt_mat)
    output = OUTPUT / (filename + '.glb')
    model.write(output)
    print(f'{output.name}: {output.stat().st_size:,} bytes, {len(model.meshes)} mesh pieces')


if __name__ == '__main__':
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for entry in WINES:
        build(*entry)
