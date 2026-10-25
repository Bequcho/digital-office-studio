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
projection removes their rectangular seams. Each reverse side now has a unique,
photorealistic **AI-designed back-view studio image**, whose smaller
counterlabel matches the particular wine and the front's glass and capsule
palette. The original concept reverses remain in `rear-source/`; a second,
more sophisticated set with detailed Kakhetian vineyard and qvevri engravings,
textured paper and restrained gold foiling lives in `rear-premium/` and is used
by the current models. The original front photographs remain unchanged.
The intervening side angles use a smooth studio-glass reconstruction. Each
`.glb` contains its own complete 360° texture; no extra image requests are
needed at viewing time.

**Accuracy:** These models combine an original front photograph with an
AI-generated concept rear. They are not multi-camera product scans. The rear
counterlabels are **design concepts, not verified real-world packaging** and
must not be presented as product-compliance or manufacturer-approved labels.
No invented producer address, barcode, alcohol percentage, certifications or
importer information has been added. The hidden side surfaces are reconstructed.

The `*-label.webp` and `*-cap.webp` files are low-bandwidth curved CSS viewer
fallback textures. They are not required by the standalone `.glb` files.

Regenerate the models with `python tools/build_kakheti_models.py` using the
original local front photos and checked-in `rear-premium/` images; run
`python tools/test_kakheti_glb.py` to verify them.
