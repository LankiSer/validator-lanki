import uuid
from io import BytesIO
from pathlib import Path

from fastapi import HTTPException, UploadFile, status
from PIL import Image

from app.core.config import settings

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
IMAGE_SIZE = (300, 200)


async def save_upload(file: UploadFile) -> str:
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Разрешены только изображения (JPEG, PNG, WebP, GIF).",
        )

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    content = await file.read()
    try:
        image = Image.open(BytesIO(content))
        image = image.convert("RGB")
        image.thumbnail(IMAGE_SIZE, Image.Resampling.LANCZOS)
    except Exception as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Некорректный файл изображения") from exc

    filename = f"{uuid.uuid4().hex}.jpg"
    path = upload_dir / filename
    image.save(path, format="JPEG", quality=90)
    return f"/uploads/{filename}"


def delete_upload(image_url: str | None) -> None:
    if not image_url or not image_url.startswith("/uploads/"):
        return
    path = Path(settings.upload_dir) / Path(image_url).name
    if path.exists():
        path.unlink()
