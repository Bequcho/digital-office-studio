"""Structural check for all Kakheti Wine House glTF binary assets."""
import json
import struct
from pathlib import Path

MODELS = Path(__file__).resolve().parents[1] / 'assets' / 'models'
files = sorted(MODELS.glob('*.glb'))
assert len(files) == 6, f'Expected six bottles, got {len(files)}'

for path in files:
    contents = path.read_bytes()
    magic, version, total = struct.unpack_from('<III', contents)
    assert magic == 0x46546C67 and version == 2 and total == len(contents)
    json_size, json_type = struct.unpack_from('<I4s', contents, 12)
    assert json_type == b'JSON'
    gltf = json.loads(contents[20:20+json_size])
    bin_offset = 20+json_size
    bin_size, bin_type = struct.unpack_from('<I4s', contents, bin_offset)
    assert bin_type == b'BIN\0'
    assert bin_size == len(contents) - bin_offset - 8
    assert len(gltf['meshes']) == 1
    assert len(gltf['images']) == 1
    assert all(item['mimeType'] == 'image/jpeg' for item in gltf['images'])
    assert 'Photographic front and generated back' in gltf['extras']['accuracy']
    assert gltf['extras']['labelStatus'].startswith('Rear label design concept')
    assert gltf['accessors'][0]['count'] >= 2000
    for accessor in gltf['accessors']:
        assert accessor['count'] > 0
        view = gltf['bufferViews'][accessor['bufferView']]
        assert view.get('byteOffset',0) + view['byteLength'] <= bin_size
    for img in gltf['images']:
        view = gltf['bufferViews'][img['bufferView']]
        start = bin_offset+8+view['byteOffset']
        assert contents[start:start+3] == b'\xff\xd8\xff'
    print(f'VALID: {path.name}, {len(contents):,} bytes')
