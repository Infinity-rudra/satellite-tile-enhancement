import argparse
from pathlib import Path

import cv2
import numpy as np


def resize_for_display(image, size=(480, 480)):
    """Resize an image for a consistent comparison grid."""
    return cv2.resize(image, size, interpolation=cv2.INTER_AREA)


def add_label(image, label):
    """Add a readable title above an image."""
    height, width = image.shape[:2]

    canvas = np.full(
        (height + 45, width, 3),
        255,
        dtype=np.uint8,
    )

    canvas[45:, :] = image

    cv2.putText(
        canvas,
        label,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    return canvas


def main():
    parser = argparse.ArgumentParser(
        description="Create a visual comparison of satellite enhancement methods"
    )

    parser.add_argument(
        "--input",
        default="data/building_076747_mapbox.png",
        help="Path to the original image",
    )

    parser.add_argument(
        "--output",
        default="comparison_sr.png",
        help="Output comparison image path",
    )

    parser.add_argument(
        "--model",
        default="models/EDSR_x2.pb",
        help="Path to the pretrained EDSR x2 model",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    model_path = Path(args.model)

    if not input_path.is_file():
        raise SystemExit(f"Input image not found: {input_path}")

    if not model_path.is_file():
        raise SystemExit(f"EDSR model not found: {model_path}")

    original = cv2.imread(str(input_path))

    if original is None:
        raise SystemExit("Could not read the input image.")

    height, width = original.shape[:2]

    # Simulate a low-resolution input.
    low_resolution = cv2.resize(
        original,
        (max(1, width // 2), max(1, height // 2)),
        interpolation=cv2.INTER_AREA,
    )

    # Bicubic reconstruction.
    bicubic = cv2.resize(
        low_resolution,
        (width, height),
        interpolation=cv2.INTER_CUBIC,
    )

    # Classical enhancement using the existing pipeline.
    from enhance import enhance_image

    classical = enhance_image(bicubic)

    # Pretrained EDSR x2 reconstruction.
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(model_path))
    sr.setModel("edsr", 2)

    edsr = sr.upsample(low_resolution)

    if edsr.shape[:2] != original.shape[:2]:
        edsr = cv2.resize(
            edsr,
            (width, height),
            interpolation=cv2.INTER_CUBIC,
        )

    # Prepare a common display size.
    images = [
        ("Original", original),
        ("Bicubic", bicubic),
        ("Classical", classical),
        ("EDSR x2", edsr),
    ]

    panels = []

    for label, image in images:
        display_image = resize_for_display(image)
        panels.append(add_label(display_image, label))

    # Arrange panels in a 2x2 grid.
    top_row = np.hstack((panels[0], panels[1]))
    bottom_row = np.hstack((panels[2], panels[3]))

    comparison = np.vstack((top_row, bottom_row))

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), comparison):
        raise SystemExit(f"Could not save comparison: {output_path}")

    print(f"Original image: {input_path.name}")
    print(f"Comparison saved to: {output_path.resolve()}")
    print(f"Grid dimensions: {comparison.shape[1]} x {comparison.shape[0]}")


if __name__ == "__main__":
    main()