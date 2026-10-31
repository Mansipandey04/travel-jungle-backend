import uuid
from pathlib import Path

from app.storage.base import StorageBackend

ALLOWED_MIME = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


class LocalStorage(StorageBackend):
    def __init__(self, root: str, public_base_url: str = "http://localhost:8000") -> None:
        self.root = Path(root)
        self.public_base_url = public_base_url.rstrip("/")
        self.root.mkdir(parents=True, exist_ok=True)

    def save(self, *, filename: str, content: bytes, content_type: str) -> str:
        ext = ALLOWED_MIME.get(content_type)
        if not ext:
            raise ValueError(f"Unsupported content type: {content_type}")
        safe_name = f"{uuid.uuid4().hex}{ext}"
        path = self.root / safe_name
        path.write_bytes(content)
        return f"{self.public_base_url}/uploads/{safe_name}"

    def delete(self, *, relative_path: str) -> None:
        name = Path(relative_path).name
        target = self.root / name
        if target.exists():
            target.unlink()
