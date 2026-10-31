"""Shared FastAPI dependencies."""

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.auth.admin import require_admin
from app.config import Settings, get_settings
from app.db import get_db
from app.storage.base import StorageBackend
from app.storage.local import LocalStorage


def get_storage(settings: Annotated[Settings, Depends(get_settings)]) -> StorageBackend:
    return LocalStorage(root=settings.upload_root, public_base_url=settings.public_base_url)


DbSession = Annotated[Session, Depends(get_db)]
AppSettings = Annotated[Settings, Depends(get_settings)]
AdminUser = Annotated[dict, Depends(require_admin)]
StorageDep = Annotated[StorageBackend, Depends(get_storage)]


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"
