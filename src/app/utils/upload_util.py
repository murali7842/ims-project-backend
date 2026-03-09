import base64
import uuid
from datetime import datetime
from pathlib import Path
from src.app.common.exception import errors
from src.app.config.setting import get_setting
from src.app.models.enum import MediaType
import aiofiles

settings = get_setting()

max_size_bytes = 25 * 1024 * 1024 * 1024

ALLOWED_MIME_TYPES = {
    ".json": "application/json",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".csv": "text/csv",
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".doc": "application/msword",
    ".ppt": "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".txt": "text/plain",
    ".md": "text/markdown",

    ".jpg": "application/jpg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".jpeg":"image/jpeg",

    ".mp4": "video/mp4",
    ".mp3": "audio/mpeg",
    ".wav": "audion/wav",
    ".weba": "audio/webm",
    ".webm": "video/webm",

    ".zip": "application/zip",
    ".rar": "application/vnd.rar",
}

# Restricted / Blocked extensions
BLOCKED_EXTENSIONS = {
    ".exe", ".msi", ".bat", ".sh", ".cmd", ".com",
    ".js", ".php", ".py", ".pl", ".rb",
    ".html", ".htm", ".css", ".jsp", ".asp",
    ".bash", ".zsh", ".ksh",
    ".dll", ".so"
}

MIME_MEDIA_TYPE_MAP = {

    "application/pdf": MediaType.DOC,
    "application/msword": MediaType.DOC,
    "text/csv": MediaType.DOC,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": MediaType.DOC,
    "application/vnd.ms-excel": MediaType.DOC,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": MediaType.DOC,
    "application/vnd.ms-powerpoint": MediaType.DOC,
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": MediaType.DOC,
    "text/plain": MediaType.DOC,
    "text/markdown": MediaType.DOC,

    "application/jpg": MediaType.IMAGE,
    "application/jpeg": MediaType.IMAGE,
    "application/png": MediaType.IMAGE,
    "image/svg+xml": MediaType.IMAGE,
    "image/jpg": MediaType.IMAGE,
    "image/jpeg": MediaType.IMAGE,
    "image/png": MediaType.IMAGE,
    "image/gif": MediaType.IMAGE,

    "video/mp4": MediaType.VIDEO,
    "audio/mpeg": MediaType.AUDIO,
    "audio/wav": MediaType.AUDIO,
    "audio/webm": MediaType.AUDIO,
    "video/webm": MediaType.VIDEO,
    "video/mpeg": MediaType.VIDEO,

    "application/zip": MediaType.DOC,
    "application/vnd.rar": MediaType.DOC,
}
def generate_unique_filename(ext: str) -> str:
    """Generate a unique filename with timestamp and UUID."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}{ext}"

async def save_base64_to_file(base64_string: str, loc: Path) -> dict:
    # Extract the image format and actual Base64 data
    header, encoded = base64_string.split(",", 1) if "," in base64_string else ("", base64_string)

    # Extract mime type from header
    if header.startswith("data:") and ";" in header:
        mime = header.split(";")[0].replace("data:", "")
    else:
        raise errors.NotFoundError(msg="Invalid or missing MIME type in base64 string")

    # Raise error if MIME type is not supported
    if mime not in MIME_MEDIA_TYPE_MAP:
        errors.NotFoundError(msg="Unsupported MIME type: {mime}")

    # Find file extension by matching mime from ALLOWED_MIME_TYPES dict (reverse lookup)
    extension = next(
        (ext for ext, mimes in ALLOWED_MIME_TYPES.items() if mime in (mimes if isinstance(mimes, list) else [mimes])),
        None
    )
    if not extension:
        errors.NotFoundError(msg="No file extension mapped for MIME type: {mime}")

    # Decode the base64 content
    file_data = base64.b64decode(encoded)

    file_size = file_data.__sizeof__()

    # Generate a unique filename
    filename = generate_unique_filename(extension)


    # Prepare the full save location
    full_loc = Path(f"{settings.IMAGES_PATH}{loc}")
    full_loc.mkdir(parents=True, exist_ok=True)
    file_path = full_loc / filename

    # Save the file asynchronously
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(file_data)

    # Media type from MIME_MEDIA_TYPE_MAP
    media_type = MIME_MEDIA_TYPE_MAP[mime]

    # Return all required info
    return {
        "name": filename,
        "loc": str(loc / filename),
        "size": file_size,
        "type": media_type,
        "mime": mime
    }