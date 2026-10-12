import argparse
from pathlib import Path

import cv2


def enhance_image(image):
    """Classical image enhancement using denoising, CLAHE and sharpening."""

    # Reduce noise while preserving edges
    denoised = cv2.bilateralFilter(image, 5, 20, 20)

    # Improve local contrast in LAB colour space
    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=1.3,
        tileGridSize=(8, 8),
    )
    l = clahe.apply(l)

    enhanced = cv2.cvtColor(
        cv2.merge((l, a, b)),
        cv2.COLOR_LAB2BGR,
    )

    # Apply mild sharpening
    blurred = cv2.GaussianBlur(enhanced, (0, 0), 1.0)
    sharpened = cv2.addWeighted(
        enhanced,
        1.15,
        blurred,
        -0.15,
        0,
    )

    return sharpened


def load_edsr_model(model_path):
    """Load the pretrained EDSR x2 super-resolution model."""

    if not model_path.is_file():
        raise FileNotFoundError(
            f"EDSR model not found: {model_path}"
        )

    if not hasattr(cv2, "dnn_superres"):
        raise RuntimeError(
            "OpenCV dnn_superres is unavailable. "
            "Install opencv-contrib-python in your active environment."
        )

    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(str(model_path))
    sr.setModel("edsr", 2)

    return sr


def main():
    parser = argparse.ArgumentParser(
        description="Satellite image enhancement and super-resolution"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Folder containing input images",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Folder where processed images will be saved",
    )

    parser.add_argument(
        "--method",
        choices=["classical", "edsr"],
        default="classical",
        help="Processing method: classical enhancement or EDSR x2",
    )

    parser.add_argument(
        "--model",
        default="models/EDSR_x2.pb",
        help="Path to the pretrained EDSR x2 model",
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    model_path = Path(args.model)

    if not input_dir.is_dir():
        raise SystemExit(
            f"Input directory does not exist: {input_dir}"
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    extensions = {".jpg", ".jpeg", ".png"}

    files = sorted(
        path
        for path in input_dir.iterdir()
        if path.is_file()
        and path.suffix.lower() in extensions
    )

    if not files:
        raise SystemExit(
            f"No images found in {input_dir}"
        )

    # Load the EDSR model once, not once per image.
    sr = None

    if args.method == "edsr":
        try:
            sr = load_edsr_model(model_path)
        except (FileNotFoundError, RuntimeError, cv2.error) as exc:
            raise SystemExit(str(exc)) from exc

    processed = 0
    failed = 0

    for path in files:
        image = cv2.imread(str(path))

        if image is None:
            print(f"Skipped unreadable image: {path.name}")
            failed += 1
            continue

        try:
            if args.method == "classical":
                result = enhance_image(image)

            else:
                # EDSR x2 doubles both width and height.
                result = sr.upsample(image)

        except cv2.error as exc:
            print(f"Processing failed for {path.name}: {exc}")
            failed += 1
            continue

        output_path = output_dir / path.name

        if not cv2.imwrite(str(output_path), result):
            print(f"Failed to save: {path.name}")
            failed += 1
            continue

        processed += 1
        print(
            f"Processed: {path.name} | "
            f"Method: {args.method} | "
            f"Output size: {result.shape[1]}x{result.shape[0]}"
        )

    print("\nProcessing completed.")
    print(f"Method: {args.method}")
    print(f"Images processed: {processed}")
    print(f"Images skipped/failed: {failed}")
    print(f"Output folder: {output_dir.resolve()}")


if __name__ == "__main__":
    main()