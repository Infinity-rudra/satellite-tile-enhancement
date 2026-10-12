from pathlib import Path
from io import BytesIO

import cv2
import numpy as np

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import Response


app = FastAPI(
    title="Satellite Tile Enhancement API",
    description=(
        "Enhance satellite images using classical image processing "
        "or pretrained EDSR x2 super-resolution."
    ),
    version="1.0.0",
)

# Pretrained EDSR model location
MODEL_PATH = Path("models") / "EDSR_x2.pb"

# Upload limit: 15 MB
MAX_FILE_SIZE = 15 * 1024 * 1024

# Lazy model loading: load EDSR only when first requested
sr_model = None


def enhance_classical(image: np.ndarray) -> np.ndarray:
    """Denoise, improve local contrast and sharpen the image."""

    denoised = cv2.bilateralFilter(image, 5, 20, 20)

    lab = cv2.cvtColor(denoised, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=1.3,
        tileGridSize=(8, 8),
    )

    l_channel = clahe.apply(l_channel)

    enhanced = cv2.cvtColor(
        cv2.merge((l_channel, a_channel, b_channel)),
        cv2.COLOR_LAB2BGR,
    )

    blurred = cv2.GaussianBlur(enhanced, (0, 0), 1.0)

    sharpened = cv2.addWeighted(
        enhanced,
        1.15,
        blurred,
        -0.15,
        0,
    )

    return sharpened


def load_edsr_model():
    """Load the pretrained EDSR x2 model on demand."""

    global sr_model

    if sr_model is not None:
        return sr_model

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"EDSR model not found at {MODEL_PATH.resolve()}. "
            "Download EDSR_x2.pb and place it in the models folder."
        )

    if not hasattr(cv2, "dnn_superres"):
        raise RuntimeError(
            "OpenCV super-resolution module is unavailable. "
            "Install opencv-contrib-python."
        )

    model = cv2.dnn_superres.DnnSuperResImpl_create()
    model.readModel(str(MODEL_PATH))
    model.setModel("edsr", 2)

    sr_model = model
    return sr_model


def enhance_edsr(image: np.ndarray) -> np.ndarray:
    """Apply pretrained EDSR x2 super-resolution."""

    model = load_edsr_model()
    return model.upsample(image)


def decode_image(image_bytes: bytes) -> np.ndarray:
    """Decode uploaded image bytes into an OpenCV image."""

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(image_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Maximum upload size is 15 MB.",
        )

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image. Please upload a valid PNG, JPEG, or WEBP image.",
        )

    return image


@app.get("/")
def home():
    return {
        "message": "Satellite Tile Enhancement API is running.",
        "documentation": "/docs",
        "endpoint": "POST /enhance",
        "supported_methods": ["classical", "edsr"],
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "edsr_model_loaded": sr_model is not None,
    }


@app.post("/enhance")
async def enhance(
    file: UploadFile = File(...),
    method: str = Query(
        default="classical",
        pattern="^(classical|edsr)$",
        description="Choose classical enhancement or EDSR x2 super-resolution.",
    ),
):
    """Accept an image and return the enhanced image as PNG."""

    try:
        image_bytes = await file.read()

        image = decode_image(image_bytes)

        if method == "classical":
            result = enhance_classical(image)
        elif method == "edsr":
            result = enhance_edsr(image)
        else:
            raise HTTPException(
                status_code=400,
                detail="Method must be classical or edsr.",
            )

        success, encoded_image = cv2.imencode(".png", result)

        if not success:
            raise HTTPException(
                status_code=500,
                detail="Failed to encode the enhanced image.",
            )

        return Response(
            content=encoded_image.tobytes(),
            media_type="image/png",
            headers={
                "Content-Disposition": (
                    'attachment; filename="enhanced.png"'
                )
            },
        )

    except HTTPException:
        raise

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Image enhancement failed: {exc}",
        ) from exc

    finally:
        await file.close()