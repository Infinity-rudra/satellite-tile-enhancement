# Satellite Tile Enhancement

A Python-based computer vision project for enhancing satellite and aerial imagery using classical image processing and pretrained 2× super-resolution.

This project was developed for the Satellite Tile Enhancement take-home assignment.

## 1. Project Objectives

The project implements and evaluates three approaches:

- **Classical enhancement:** Edge-preserving denoising, local contrast enhancement, and mild sharpening.
- **Bicubic interpolation:** Baseline for 2× image upscaling.
- **EDSR x2:** Pretrained deep-learning super-resolution model.

The evaluation uses a synthetic reference because independent high-resolution ground-truth images are unavailable.

## 2. Methods

### Classical Enhancement

Implemented in `enhance.py` using OpenCV:

1. Bilateral filtering for edge-preserving denoising.
2. CLAHE on the luminance channel in LAB colour space for local contrast enhancement.
3. Mild sharpening to make boundaries more visible.

This method preserves the input image dimensions.

### Deep-Learning Super-Resolution

The EDSR x2 option uses a pretrained model through OpenCV's `dnn_superres` module.

It produces an image with twice the input width and height. The model is loaded once and reused while processing the input directory.

The model is not trained from scratch.

### Evaluation

`evaluate.py` compares Bicubic interpolation, classical enhancement, and EDSR x2 using:

- **PSNR:** Measures pixel-level similarity to the reference.
- **SSIM:** Measures structural similarity to the reference.

The synthetic protocol downsamples each original image by approximately 2× and reconstructs it. The original image is used as a synthetic reference.

These metrics are useful for comparison under the defined protocol but do not establish geographic accuracy or guarantee real-world enhancement quality.

## 3. Requirements

- Python
- NumPy
- OpenCV with `dnn_superres` support
- Pillow
- scikit-image

## 4. Installation

Clone the repository:

```bash
git clone https://github.com/Infinity-rudra/satellite-tile-enhancement.git
cd satellite-tile-enhancement
```

Create and activate a virtual environment on Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Ensure the input images are available in `data/` and the compatible pretrained EDSR x2 model is available at:

```text
models/EDSR_x2.pb
```

**Dataset:** Download the assignment dataset from the [provided Google Drive folder](https://drive.google.com/drive/folders/1oXTAUiFQPQso13NRznnecdWwj5z-cYgV) and place the input images in the `data/` directory.

**Pretrained model:** Download the pretrained `EDSR_x2.pb` model from the [Saafke/EDSR_Tensorflow repository](https://github.com/Saafke/EDSR_Tensorflow/tree/master/models). The direct download link is [EDSR_x2.pb](https://raw.githubusercontent.com/Saafke/EDSR_Tensorflow/master/models/EDSR_x2.pb). Save the file as `models/EDSR_x2.pb`.

The dataset and model are excluded from version control. Follow the applicable usage and redistribution terms before redistributing either asset.
The dataset and model are excluded from version control. Use the supplied dataset for the assignment and follow the applicable usage and redistribution terms. Do not redistribute the dataset or pretrained model unless you have permission to do so.

## 5. Usage

Run commands from the project root.

### Classical Enhancement

```bash
python enhance.py --input data/ --output out_classical/ --method classical
```

### EDSR Super-Resolution

```bash
python enhance.py --input data/ --output out_edsr/ --method edsr
```

The EDSR command requires `models/EDSR_x2.pb`.

### Evaluation

```bash
python evaluate.py --input data/ --report results_sr.md
```

The report contains per-image and aggregate PSNR/SSIM results for the implemented evaluation protocol.

### Visual Comparison

```bash
python compare_sr.py
```

This generates `comparison_sr.png`, a visual comparison of the original image, Bicubic interpolation, classical enhancement, and EDSR output.

## 6. Evaluation Results

Mean results across 41 images:

| Method | Mean PSNR (dB) | Mean SSIM |
|---|---:|---:|
| Bicubic | 32.445 | 0.9091 |
| Classical Enhancement | 25.341 | 0.8837 |
| EDSR x2 | 34.013 | 0.9210 |

EDSR achieved the highest PSNR and SSIM under this synthetic evaluation protocol.

Classical enhancement can make some boundaries appear sharper while reducing similarity to the original reference. These results should not be interpreted as proof that the model reconstructs missing real-world details accurately.

## 7. Failure Cases

Selected visual crops are provided in `failure_cases/crops/`.

The examples illustrate limitations such as:

- Fine details that remain unresolved after enhancement.
- Ambiguous boundaries and dark regions that cannot be reliably reconstructed.
- Small texture variations that become more prominent after classical enhancement but may represent either real texture or noise.

Visual examples are illustrative observations, not proof that every suspected artifact is present.

## 8. Project Structure

```text
Satellite-Tile-Enhancement/
├── data/                       # Local input images; not tracked by Git
├── models/
│   └── EDSR_x2.pb              # Local pretrained model; not tracked by Git
├── failure_cases/
│   └── crops/                  # Selected visual failure-case crops
├── enhance.py                  # Classical enhancement and EDSR inference
├── evaluate.py                 # Synthetic evaluation and metrics
├── compare_sr.py               # Visual comparison generation
├── comparison_sr.png           # Generated comparison image
├── results_sr.md               # Evaluation report
├── requirements.txt            # Python dependencies
├── WRITEUP.md                  # Technical assignment write-up
├── README.md                   # Setup and usage instructions
└── .gitignore
```

## 9. Limitations and Responsible Use

- Synthetic downsampling does not reproduce every real-world imaging degradation.
- PSNR and SSIM do not measure geographic correctness or semantic accuracy.
- Super-resolution models can generate plausible details that are not supported by the input.
- Enhanced imagery should not be treated as authoritative evidence of real-world structures without independent verification.
- Before storing, displaying, or redistributing enhanced Google Maps imagery, review the applicable Google Maps Platform terms, attribution requirements, caching restrictions, and derivative-content rules. Obtain the required permissions before deployment.

## 10. Assignment Deliverables

| Deliverable | File |
|---|---|
| Classical enhancement and super-resolution | `enhance.py` |
| Evaluation and metrics | `evaluate.py` |
| Dependency list | `requirements.txt` |
| Technical write-up | `WRITEUP.md` |
| Visual comparison | `comparison_sr.png` |
| Evaluation report | `results_sr.md` |
| Failure-case crops | `failure_cases/crops/` |

---

**Note:** The evaluation results describe the current synthetic experiment and should not be interpreted as a guarantee of performance on real degraded satellite imagery.