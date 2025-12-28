import sys, os, pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.getcwd())
from app.main import app
from app.core.config import get_settings

settings = get_settings()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c: yield c

@pytest.fixture(scope="module")
def db_session():
    engine = create_engine(settings.DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)
    db = TestingSessionLocal()
    try: yield db
    finally: db.close()
