from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

router = APIRouter(prefix="/media", tags=["Media"])

BASE_DIR = Path("media")

ALLOWED_TYPES = {
    "images": ["image/jpeg", "image/png", "image/webp"],
    "audio": ["audio/mpeg", "audio/wav", "audio/webm"],
    "videos": ["video/mp4", "video/webm"],
}

MAX_FILE_SIZE_MB = 20


def validate_file(file: UploadFile, category: str):
    if category not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid category")
    if file.content_type not in ALLOWED_TYPES[category]:
        raise HTTPException(status_code=400, detail="Invalid file type")


@router.post("/upload/{category}")
async def upload_media(category: str, file: UploadFile = File(...)):
    validate_file(file, category)

    folder = BASE_DIR / category
    folder.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{ext}"
    file_path = folder / filename

    content = await file.read()
    if len(content) / (1024 * 1024) > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail="File too large")

    with open(file_path, "wb") as f:
        f.write(content)

    return {"url": f"/media/{category}/{filename}"}
