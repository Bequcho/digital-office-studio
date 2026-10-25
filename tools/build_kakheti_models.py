"""Generate photogrammetric-style wine-bottle GLBs from catalog photography.

The *entire* photographed front (glass, highlights, label and foil) is projected
onto a curved bottle. Side/back pixels are synthesized, not represented as
photographs of previously unseen angles. The originals are required locally
outside the repository and are never bundled into the site's source tree.
"""

from __future__ import annotations

import io
import json
import math
import struct
from pathlib import Path

import numpy as np
from PIL import Image


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
        photo.save(stream, 'JPEG', quality=89, subsampling=0, optimize=True)
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
                           "accuracy": "Photographic front projection; unseen sides and back reconstructed"}}
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


def revolved(profile, divisions=160, theta_min=-math.pi, theta_max=math.pi,
             uv_mode="height"):
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
            if uv_mode == 'height':
                v = 1 - (height-profile[0][0])/(profile[-1][0]-profile[0][0])
            else:
                v = 1 - j/(len(profile)-1)
            uvs.append((u, v))
    for j in range(len(profile) - 1):
        for i in range(divisions):
            a, b = j*(divisions+1)+i, (j+1)*(divisions+1)+i
            faces += [(a, a+1, b), (a+1, b+1, b)]
    return points, normals, uvs, faces


PROFILE = [
    (.0000,.0250),(.001,.029),(.002,.033),(.004,.036),(.007,.038),(.013,.0385),
    (.035,.0385),(.062,.0385),(.132,.0385),(.177,.0385),(.196,.0385),
    # Calibrated to the *visible* outline in the studio photographs.  In those
    # shots the dark glass neck continues to ~y=360px; the shoulders do not
    # flare until ~y=380px.  The earlier shoulder began around y=300px and
    # pulled bright studio-background pixels into a conspicuous rectangle.
    (.200,.0385),(.203,.0384),(.2075,.0365),(.212,.0330),(.2167,.0292),
    (.2214,.0240),(.2248,.0210),(.229,.0170),(.234,.0153),(.246,.0153),
    (.251,.0153),(.260,.0153),
    (.283,.0153),(.297,.0153),(.300,.0162),(.302,.0163),(.304,.0160),
    (.306,.0160),(.308,.0153),(.310,.0140),
]


def make_photographic_wrap(photo, tone, foil, width=1536, height=2048):
    """Perspective-correct front projection, with a reconstructed rear hemisphere.

    A UV *height* coordinate is essential here; evenly spaced profile-row UVs
    would deform the photographed label and make the bottle look illustrated.
    """
    pixels = np.asarray(photo, dtype=np.float32)
    hh, ww = pixels.shape[:2]
    x = np.linspace(-math.pi, math.pi, width, endpoint=True, dtype=np.float32)[None, :]
    rows = np.linspace(0, 1, height, dtype=np.float32)[:, None]
    y_model = .310 * (1 - rows)
    radius = np.interp(y_model[:, 0], [p[0] for p in PROFILE],
                       [p[1] for p in PROFILE]).astype(np.float32)[:, None]
    # Coordinates were measured against the original 1122 x 1402 px catalog shots.
    yy = np.clip(20 + rows * (1348 - 20), 0, hh-1)
    xx = np.clip(ww/2 + radius * 4210 * np.sin(x), 0, ww-1)
    xi = np.rint(xx).astype(np.int32)
    yi = np.broadcast_to(np.rint(yy).astype(np.int32), (height, width))
    front = pixels[yi, np.broadcast_to(xi, (height, width))]

    foil_rgb = {
        'gold': (164., 107., 39.), 'burgundy': (85., 22., 35.),
        'black': (49., 48., 43.)
    }[foil]
    glass_rgb = (70., 34., 14.) if tone == 'amber' else (30., 12., 19.)
    # A restrained photographic studio light rig on the otherwise unseen rear.
    light_ribbon = 45*np.exp(-((x-2.12)/.17)**2) + 19*np.exp(-((x+2.40)/.13)**2)
    rear = np.empty((height, width, 3), dtype=np.float32)
    cap_mask = np.clip((y_model-.245)/.012, 0, 1)
    rear_color = np.array(glass_rgb)[None, None, :]*(1-cap_mask[:, :, None]) + \
        np.array(foil_rgb)[None, None, :]*cap_mask[:, :, None]
    rear[:] = rear_color
    rear += light_ribbon[:, :, None]*np.array([1., .86, .65])[None, None, :]
    # Glass grows darker near the heel; foil stays lustrous on top.
    heel_dim = .72 + .28*np.clip(y_model/.038, 0, 1)
    rear *= heel_dim[:, :, None]*(1-cap_mask[:, :, None]) + cap_mask[:, :, None]

    # Studio backdrop must never enter the bottle texture.  In the shoulder
    # rows the diameter changes rapidly, so even a few pixels of projection
    # mismatch used to introduce a conspicuous straight-edged beige rectangle.
    # Compare each photographed pixel with the empty backdrop at that height,
    # and replace backdrop samples by reconstructed coloured glass.  This is
    # limited to the upper glass/foil, preserving the exact paper label pixels.
    backdrop = pixels[np.broadcast_to(yi[:, :1], (height, 1)), 60, :]
    backdrop_difference = np.max(np.abs(front - backdrop), axis=2)
    foreground = np.clip((backdrop_difference - 10.0) / 30.0, 0, 1)
    foreground = foreground * foreground * (3 - 2 * foreground)
    upper_only = np.clip((540.0 - yy) / 50.0, 0, 1)
    foreground = 1 - upper_only * (1 - foreground)

    # Original photograph dominates the front. Blend out toward the unseen
    # side and any pixels that were originally photographic background.
    edge = np.clip((np.abs(x)-1.31)/.39, 0, 1)
    edge = edge*edge*(3-2*edge)
    photo_mix = (1-edge) * foreground
    wrap = front*photo_mix[:, :, None] + rear*(1-photo_mix[:, :, None])
    return Image.fromarray(np.uint8(np.clip(wrap, 0, 255)), 'RGB')


def build(filename, source, tone, foil):
    photo = Image.open(ROOT / source).convert('RGB')
    if photo.size != (1122, 1402):
        raise ValueError(f'Unexpected crop calibration for {source}: {photo.size}')

    model = Model(filename)
    wrap = make_photographic_wrap(photo, tone, foil)
    photographed = model.add_texture(wrap, 'Studio photo projection, 360 degree reconstruction')
    bottle_mat = model.material('Photographically textured '+tone+' glass and capsule',
                                (1.,1.,1.), .19, .04, texture=photographed,
                                gloss='studio softbox reflections')
    model.add_mesh('Full photographic glass silhouette', *revolved(PROFILE), bottle_mat)
    output = OUTPUT / (filename + '.glb')
    model.write(output)
    print(f'{output.name}: {output.stat().st_size:,} bytes, {len(model.meshes)} mesh pieces')


if __name__ == '__main__':
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for entry in WINES:
        build(*entry)
