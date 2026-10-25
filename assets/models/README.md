# Kakheti Wine House — 3D bottle models

Six self-contained, standards-based glTF 2.0 binary (`.glb`) files:

- `kisi-amber-2023.glb`
- `khikhvi-reserve-2022.glb`
- `rkatsiteli-qvevri-2023.glb`
- `kindzmarauli-2023.glb`
- `mukuzani-reserve-2021.glb`
- `saperavi-qvevri-2022.glb`

Each model includes a sculpted glass silhouette with bottle heel, tapered
shoulders, neck and capsule. A **height-calibrated photographic projection** of
the entire front of the source bottle wraps its surface: the original glass
highlights, exact label lettering, color and foil are captured together.
Previously the label and foil were separate flat-looking overlays; the new
projection removes their rectangular seams. Back and hidden sides have a
subdued studio-light reconstruction. No additional image requests are needed.

**Accuracy:** These are **single-photo-based reconstructions**, not multi-camera
360° product scans. True side and back photography and authentic reverse labels
were not available. The front is photographic; the rear is visually plausible
but not a documentary reproduction. This is a concept collection.

The `*-label.webp` and `*-cap.webp` files are low-bandwidth curved CSS viewer
fallback textures. They are not required by the standalone `.glb` files.

Regenerate the models with `python tools/build_kakheti_models.py` from the
original bottle photos; run `python tools/test_kakheti_glb.py` to verify them.
