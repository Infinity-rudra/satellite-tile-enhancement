# Satellite Tile Enhancement Evaluation

**Images evaluated:** 41

## Evaluation Protocol

Each original image is used as a synthetic reference. The image is downscaled by approximately 2x using area interpolation. Bicubic reconstruction and EDSR x2 are applied to the low-resolution image. Classical enhancement is applied to the Bicubic reconstruction.

PSNR and SSIM compare each output against the original image. Higher values indicate greater pixel-level or structural similarity to this reference.

## Per-Image Results

| Image | Bicubic PSNR | Bicubic SSIM | Classical PSNR | Classical SSIM | EDSR PSNR | EDSR SSIM |
|---|---:|---:|---:|---:|---:|---:|
| building_076747_mapbox.png | 39.030 | 0.9882 | 27.257 | 0.9583 | 41.089 | 0.9918 |
| building_1e44ba_google.png | 27.509 | 0.8849 | 23.437 | 0.8745 | 28.534 | 0.9073 |
| building_20d961_google.png | 25.683 | 0.5673 | 24.518 | 0.5685 | 26.913 | 0.5678 |
| building_22cade_mapbox.png | 40.110 | 0.9935 | 31.070 | 0.9795 | 41.711 | 0.9949 |
| building_3d9b33_google.png | 25.652 | 0.8411 | 22.361 | 0.8279 | 28.010 | 0.9076 |
| building_418c44_mapbox.png | 41.500 | 0.9933 | 29.137 | 0.9705 | 43.616 | 0.9952 |
| building_43ebf7_mapbox.png | 33.990 | 0.9806 | 27.058 | 0.9515 | 36.415 | 0.9881 |
| building_4efaf9_mapbox.png | 39.116 | 0.9902 | 28.619 | 0.9647 | 40.699 | 0.9928 |
| building_513098_mapbox.png | 40.102 | 0.9922 | 28.668 | 0.9737 | 42.503 | 0.9946 |
| building_57c41d_mapbox.png | 42.254 | 0.9894 | 25.466 | 0.9280 | 43.690 | 0.9912 |
| building_57c7e8_mapbox.png | 40.856 | 0.9924 | 29.247 | 0.9737 | 41.818 | 0.9933 |
| building_5aca8b_google.png | 28.519 | 0.8764 | 24.662 | 0.8801 | 29.181 | 0.8854 |
| building_666e65_google.png | 27.230 | 0.8938 | 25.574 | 0.8934 | 27.946 | 0.9065 |
| building_686199_google.png | 28.267 | 0.8238 | 25.328 | 0.8290 | 28.724 | 0.8315 |
| building_6c1ccc_mapbox.png | 39.558 | 0.9919 | 29.464 | 0.9763 | 42.331 | 0.9949 |
| building_6c8fd5_google.png | 32.067 | 0.9491 | 26.383 | 0.9321 | 33.675 | 0.9608 |
| building_7345ba_google.png | 25.511 | 0.7911 | 23.818 | 0.8027 | 25.803 | 0.7973 |
| building_761669_google.png | 27.553 | 0.8520 | 25.886 | 0.8509 | 28.469 | 0.8654 |
| building_7d9f17_mapbox.png | 38.360 | 0.9901 | 30.204 | 0.9701 | 40.240 | 0.9930 |
| building_7ecfdc_google.png | 25.523 | 0.8609 | 21.707 | 0.8348 | 26.925 | 0.8807 |
| building_814230_mapbox.png | 37.278 | 0.9855 | 27.363 | 0.9558 | 38.947 | 0.9889 |
| building_8899da_google.png | 28.554 | 0.9342 | 17.830 | 0.8351 | 31.537 | 0.9605 |
| building_8aeff0_mapbox.png | 42.396 | 0.9962 | 30.357 | 0.9843 | 44.613 | 0.9972 |
| building_8d05f2_google.png | 33.127 | 0.9649 | 29.721 | 0.9543 | 35.140 | 0.9749 |
| building_90435e_google.png | 22.468 | 0.7039 | 20.392 | 0.7341 | 23.117 | 0.7325 |
| building_98fa77_google.png | 26.806 | 0.9224 | 25.449 | 0.9144 | 27.804 | 0.9361 |
| building_a3a517_google.png | 26.830 | 0.8232 | 25.514 | 0.8261 | 27.726 | 0.8356 |
| building_a90908_google.png | 25.683 | 0.7996 | 23.964 | 0.8110 | 26.009 | 0.8077 |
| building_aba1eb_google.png | 28.182 | 0.8975 | 14.118 | 0.7191 | 30.964 | 0.9348 |
| building_b31756_google.png | 28.491 | 0.8908 | 24.846 | 0.8733 | 30.228 | 0.9188 |
| building_b31756_mapbox.png | 37.532 | 0.9856 | 25.331 | 0.9407 | 40.112 | 0.9904 |
| building_c85563_google.png | 29.158 | 0.9484 | 24.974 | 0.9269 | 31.167 | 0.9641 |
| building_c85563_mapbox.png | 37.483 | 0.9894 | 27.367 | 0.9673 | 39.110 | 0.9921 |
| building_cac04a_google.png | 25.105 | 0.8686 | 18.670 | 0.7058 | 27.222 | 0.9083 |
| building_d87dbc_google.png | 25.630 | 0.8607 | 22.428 | 0.8544 | 26.579 | 0.8830 |
| building_dc7b9e_mapbox.png | 38.923 | 0.9907 | 27.152 | 0.9494 | 40.332 | 0.9921 |
| building_e42da1_google.png | 24.370 | 0.7340 | 21.081 | 0.7378 | 25.251 | 0.7613 |
| building_f28a5f_google.png | 27.572 | 0.8478 | 25.941 | 0.8286 | 28.923 | 0.8459 |
| building_f73de6_google.png | 31.762 | 0.9030 | 23.757 | 0.8624 | 32.978 | 0.9064 |
| building_f73de6_mapbox.png | 41.756 | 0.9923 | 27.090 | 0.9455 | 44.243 | 0.9936 |
| building_fc48ee_mapbox.png | 42.731 | 0.9939 | 25.785 | 0.9641 | 44.230 | 0.9952 |

## Aggregate Results

| Method | Mean PSNR (dB) | Mean SSIM |
|---|---:|---:|
| Bicubic | 32.445 | 0.9091 |
| Classical Enhancement | 25.341 | 0.8837 |
| EDSR x2 | 34.013 | 0.9210 |

## Limitations

- The original images are synthetic references, not independent high-quality ground truth.
- Synthetic downscaling does not reproduce all real-world satellite image degradation.
- PSNR and SSIM do not fully capture perceived sharpness, geographic accuracy, or semantic correctness.
- Learned super-resolution may generate plausible details that are not present in the source image.
