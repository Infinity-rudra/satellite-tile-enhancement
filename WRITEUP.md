# Satellite Tile Enhancement --- Technical Write-up

## Pipeline

The classical pipeline applies bilateral filtering for edge-preserving
denoising, CLAHE in LAB colour space for local contrast, and mild
sharpening. EDSR x2 is a separate pretrained super-resolution option; it
is not trained from scratch. Bicubic interpolation is the baseline. The
methods are selectable through `enhance.py`.

## Evaluation and Results

With no independent high-resolution ground truth, each source image was
synthetically downscaled by approximately 2x using area interpolation.
Bicubic reconstruction and EDSR x2 were compared with the original;
classical enhancement was applied to the bicubic reconstruction. Mean
results across 41 images:

  Method        Mean PSNR (dB)   Mean SSIM
  ----------- ---------------- -----------
  Bicubic               32.445      0.9091
  Classical             25.341      0.8837
  EDSR x2               34.013      0.9210

EDSR scored highest under this synthetic protocol. Classical enhancement
looked sharper in some visual examples, but had lower reference-based
metrics. PSNR/SSIM measure similarity to the synthetic reference, not
geographic correctness or perceived quality. Synthetic downscaling does
not reproduce all real-world degradation; EDSR may generate plausible
but unsupported details. These results do not prove performance on real
degraded imagery.

## Failure Cases and Visual Observations

1.  **Limited fine-detail recovery --- `building_076747_mapbox.png`:**
    Classical enhancement makes some boundaries more prominent, but does
    not establish that missing structural details have been recovered.
    EDSR shows limited visible difference in the displayed comparison.
2.  **Ambiguous low-resolution structures ---
    `building_b31756_mapbox.png`:** Blurred boundaries and dark regions
    remain difficult to interpret after processing. Sharpening or
    super-resolution cannot guarantee accurate recovery of original
    geometry.
3.  **Texture amplification --- `building_f73de6_mapbox.png`:**
    Classical enhancement makes small roof-texture variations more
    prominent. These may be real texture, noise, or both; the visual
    comparison cannot reliably distinguish them.

The accompanying crop images illustrate these observations; they should
be interpreted as limitations, not proof that every suspected artifact
is present.

## Scaling to 50,000 Tiles/Day

50,000 tiles per day averages about 0.58 tiles/second over 24 hours.
Benchmark representative tile sizes and model latency before sizing
CPU/GPU capacity. Use a queue, bounded parallel workers, batch
processing where supported, object storage, retries with limits,
logging, monitoring, and model/version metadata. Capacity planning must
include peak load, failures, I/O, and operational overhead.

## Google Maps Terms of Service

Before storing, displaying, or redistributing enhanced Google Maps
tiles, review the current applicable Google Maps Platform terms,
attribution requirements, caching limits, and derivative-content
restrictions. Access to imagery does not automatically grant permission
to retain or redistribute processed tiles. Confirm the intended use with
the relevant legal/compliance owner before deployment.
