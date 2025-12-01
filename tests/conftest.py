import os
import pytest

# default test database if not provided
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from app.database import Base, engine, SessionLocal  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()
