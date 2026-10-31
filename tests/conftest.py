import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Configure test settings before app import side effects re-read settings.
os.environ["DATABASE_URL"] = "sqlite+pysqlite://"
os.environ["ADMIN_API_TOKEN"] = "test-admin-token"
os.environ["SEED_DEMO"] = "false"
os.environ["UPLOAD_ROOT"] = "/tmp/tj-test-uploads"
os.environ["RATE_LIMIT_SUBMISSIONS_PER_MIN"] = "1000"
os.environ["CORS_ORIGINS"] = "http://testserver"

from app.config import get_settings

get_settings.cache_clear()

from app.db import Base, get_db
from app.main import app as fastapi_app
import app.models  # noqa: F401
from app.rate_limit import limiter


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite+pysqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session: Session) -> Generator[TestClient, None, None]:
    limiter._hits.clear()

    def _override_db():
        try:
            yield db_session
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = _override_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


@pytest.fixture()
def admin_headers() -> dict[str, str]:
    return {"Authorization": "Bearer test-admin-token"}
