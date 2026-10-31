from abc import ABC, abstractmethod


class StorageBackend(ABC):
    @abstractmethod
    def save(self, *, filename: str, content: bytes, content_type: str) -> str:
        """Persist bytes and return a public URL path."""

    @abstractmethod
    def delete(self, *, relative_path: str) -> None:
        """Delete an object if present."""
