import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["LOGISTICS_A_URL"] = "http://testserver-a/api/logistics-a"
os.environ["LOGISTICS_B_URL"] = "http://testserver-b/api/logistics-b"

from fastapi.testclient import TestClient

from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.main import app
from backend.deps import get_db

pytest_plugins = [
    "fixtures.sample_database_data",
    "fixtures.sample_data",
]


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine"""
    engine = create_engine(
        os.getenv("DATABASE_URL"),
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    SQLModel.metadata.create_all(engine)    
    yield engine    
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session"""
    with Session(db_engine) as session:
        yield session


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database dependency"""
    def override_get_session():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_session
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
