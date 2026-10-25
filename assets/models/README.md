# Kakheti Wine House — 3D bottle models

Six self-contained, standards-based glTF 2.0 binary (`.glb`) files:

- `kisi-amber-2023.glb`
- `khikhvi-reserve-2022.glb`
- `rkatsiteli-qvevri-2023.glb`
- `kindzmarauli-2023.glb`
- `mukuzani-reserve-2021.glb`
- `saperavi-qvevri-2022.glb`

Each model includes a sculpted cylindrical glass mesh, tapered shoulders,
neck, capsule, heel, and curved labels. The *front label and capsule artwork*
is sampled from the corresponding Kakheti Wine House product photo and embedded
in the GLB; no additional image requests are needed to load the model.

**Accuracy:** These are 3D reconstructions from one frontal source photo per
wine. Real measurements, hidden side details, and authentic reverse labels
were not available. This is a concept collection, not photogrammetry of real
commercial bottles or an exact manufacturing CAD model.

The `*-label.webp` and `*-cap.webp` files are low-bandwidth curved CSS viewer
fallback textures. They are not required by the standalone `.glb` files.

Regenerate the models with `python tools/build_kakheti_models.py` from the
original bottle photos; run `python tools/test_kakheti_glb.py` to verify them.
