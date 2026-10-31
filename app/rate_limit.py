"""Simple in-memory IP rate limiter for public POST endpoints (MVP)."""

from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status

from app.config import get_settings
from app.deps import client_ip


class SlidingWindowLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: float = 60.0) -> None:
        now = monotonic()
        with self._lock:
            q = self._hits[key]
            while q and now - q[0] > window_seconds:
                q.popleft()
            if len(q) >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded. Try again shortly.",
                )
            q.append(now)


limiter = SlidingWindowLimiter()


async def rate_limit_submissions(request: Request) -> None:
    settings = get_settings()
    ip = client_ip(request)
    limiter.check(f"submit:{ip}", settings.rate_limit_submissions_per_min)
