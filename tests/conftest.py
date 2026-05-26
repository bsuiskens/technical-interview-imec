from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest
import os

from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app



load_dotenv()

TEST_DATABASE_URL = os.getenv(
    "DATABASE_TEST_URL",
    "sqlite:///./test.db"
)

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():

    with TestClient(app) as c:
        yield c