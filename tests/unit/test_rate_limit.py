import os

import pytest
from fastapi import HTTPException

from app.config import get_settings
from app.rate_limit import SlidingWindowLimiter


def test_rate_limit_blocks(monkeypatch):
    monkeypatch.setenv("RATE_LIMIT_SUBMISSIONS_PER_MIN", "2")
    get_settings.cache_clear()
    lim = SlidingWindowLimiter()
    lim.check("k", 2)
    lim.check("k", 2)
    with pytest.raises(HTTPException) as exc:
        lim.check("k", 2)
    assert exc.value.status_code == 429
    get_settings.cache_clear()
