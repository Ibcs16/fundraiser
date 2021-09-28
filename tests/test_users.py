from fastapi.testclient import TestClient
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import pytest


from app import __version__
from app.main import app
from app.dependencies import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# @pytest.fixture()
# def test_db():
    
#     yield
#     Base.metadata.drop_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post('/users/', json = {
            'name': 'fake-user-name',
            'email': 'fake-email',
            'password': 'fake-pwd'
        })
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'name': 'fake-user-name',
        'email': 'fake-email',
        'hashed_password': 'not so random'
    }

@pytest.mark.asyncio
async def test_create_user_with_same_email():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post('/users/', json = {
            'name': 'fake-user-name',
            'email': 'fake-same-email',
            'password': 'fake-pwd'
        })
        response2 = await ac.post('/users/', json = {
            'name': 'fake-user-name-2',
            'email': 'fake-same-email',
            'password': 'fake-pwd-2'
        })
    assert response2.status_code == 400
