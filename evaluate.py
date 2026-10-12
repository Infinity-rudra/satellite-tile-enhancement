import argparse
from pathlib import Path

import cv2
import numpy as np
from skimage.metrics import (
    peak_signal_noise_ratio,
    structural_similarity,
)

from enhance import enhance_image


def calculate_metrics(reference, result):
    """Calculate PSNR and SSIM against a reference image."""

    reference_rgb = cv2.cvtColor(reference, cv2.COLOR_BGR2RGB)
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    psnr = peak_signal_noise_ratio(
        reference_rgb,
        result_rgb,
        data_range=255,
    )

    ssim = structural_similarity(
        reference_rgb,
        result_rgb,
        channel_axis=2,
        data_range=255,
    )

    return psnr, ssim


def main():
    parser = argparse.ArgumentParser(
        description="Compare Bicubic, Classical and EDSR enhancement"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Directory containing input images",
    )

    parser.add_argument(
        "--report",
        default="results_sr.md",
        help="Path to save the Markdown report",
    )

    parser.add_argument(
        "--model",
        default="models/EDSR_x2.pb",
        help="Path to the pretrained EDSR x2 model",
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    model_path = Path(args.model)
    report_path = Path(args.report)

    if not input_dir.is_dir():
        raise SystemExit(f"Input directory not found: {input_dir}")

    if not model_path.is_file():
        raise SystemExit(f"EDSR model not found: {model_path}")

    image_files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".png", ".jpg", ".jpeg"}
    )

    if not image_files:
        raise SystemExit(f"No images found in: {input_dir}")

    # Load pretrained EDSR x2.
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(model_path))
    sr.setModel("edsr", 2)

    results = []

    for image_path in image_files:
        image = cv2.imread(str(image_path))

        if image is None:
            print(f"Skipped unreadable image: {image_path.name}")
            continue

        height, width = image.shape[:2]

        if min(height, width) < 4:
            print(f"Skipped image that is too small: {image_path.name}")
            continue

        # Create a synthetic low-resolution input.
        low_resolution = cv2.resize(
            image,
            (max(1, width // 2), max(1, height // 2)),
            interpolation=cv2.INTER_AREA,
        )

        # Method 1: Bicubic reconstruction.
        bicubic = cv2.resize(
            low_resolution,
            (width, height),
            interpolation=cv2.INTER_CUBIC,
        )

        # Method 2: Classical enhancement of Bicubic output.
        classical = enhance_image(bicubic)

        # Method 3: EDSR x2 reconstruction.
        edsr = sr.upsample(low_resolution)

        # All results should match the reference dimensions.
        if edsr.shape[:2] != image.shape[:2]:
            edsr = cv2.resize(
                edsr,
                (width, height),
                interpolation=cv2.INTER_CUBIC,
            )

        bicubic_psnr, bicubic_ssim = calculate_metrics(
            image, bicubic
        )

        classical_psnr, classical_ssim = calculate_metrics(
            image, classical
        )

        edsr_psnr, edsr_ssim = calculate_metrics(
            image, edsr
        )

        results.append(
            {
                "image": image_path.name,
                "bicubic_psnr": bicubic_psnr,
                "bicubic_ssim": bicubic_ssim,
                "classical_psnr": classical_psnr,
                "classical_ssim": classical_ssim,
                "edsr_psnr": edsr_psnr,
                "edsr_ssim": edsr_ssim,
            }
        )

        print(
            f"Evaluated: {image_path.name} | "
            f"Bicubic PSNR: {bicubic_psnr:.2f} | "
            f"Classical PSNR: {classical_psnr:.2f} | "
            f"EDSR PSNR: {edsr_psnr:.2f}"
        )

    if not results:
        raise SystemExit("No readable images were evaluated.")

    def mean(key):
        return float(np.mean([row[key] for row in results]))

    lines = [
        "# Satellite Tile Enhancement Evaluation",
        "",
        f"**Images evaluated:** {len(results)}",
        "",
        "## Evaluation Protocol",
        "",
        "Each original image is used as a synthetic reference. "
        "The image is downscaled by approximately 2x using area "
        "interpolation. Bicubic reconstruction and EDSR x2 are applied "
        "to the low-resolution image. Classical enhancement is applied "
        "to the Bicubic reconstruction.",
        "",
        "PSNR and SSIM compare each output against the original image. "
        "Higher values indicate greater pixel-level or structural "
        "similarity to this reference.",
        "",
        "## Per-Image Results",
        "",
        "| Image | Bicubic PSNR | Bicubic SSIM | "
        "Classical PSNR | Classical SSIM | EDSR PSNR | EDSR SSIM |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for row in results:
        lines.append(
            f"| {row['image']} "
            f"| {row['bicubic_psnr']:.3f} "
            f"| {row['bicubic_ssim']:.4f} "
            f"| {row['classical_psnr']:.3f} "
            f"| {row['classical_ssim']:.4f} "
            f"| {row['edsr_psnr']:.3f} "
            f"| {row['edsr_ssim']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Aggregate Results",
            "",
            "| Method | Mean PSNR (dB) | Mean SSIM |",
            "|---|---:|---:|",
            f"| Bicubic | {mean('bicubic_psnr'):.3f} "
            f"| {mean('bicubic_ssim'):.4f} |",
            f"| Classical Enhancement | {mean('classical_psnr'):.3f} "
            f"| {mean('classical_ssim'):.4f} |",
            f"| EDSR x2 | {mean('edsr_psnr'):.3f} "
            f"| {mean('edsr_ssim'):.4f} |",
            "",
            "## Limitations",
            "",
            "- The original images are synthetic references, not "
            "independent high-quality ground truth.",
            "- Synthetic downscaling does not reproduce all real-world "
            "satellite image degradation.",
            "- PSNR and SSIM do not fully capture perceived sharpness, "
            "geographic accuracy, or semantic correctness.",
            "- Learned super-resolution may generate plausible details "
            "that are not present in the source image.",
            "",
        ]
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print("\nEvaluation completed.")
    print(f"Images evaluated: {len(results)}")
    print(f"Report saved to: {report_path}")
    print("\nAggregate Results:")

    for method, psnr_key, ssim_key in [
        ("Bicubic", "bicubic_psnr", "bicubic_ssim"),
        ("Classical", "classical_psnr", "classical_ssim"),
        ("EDSR x2", "edsr_psnr", "edsr_ssim"),
    ]:
        print(
            f"{method}: PSNR={mean(psnr_key):.3f} dB, "
            f"SSIM={mean(ssim_key):.4f}"
        )


if __name__ == "__main__":
    main()