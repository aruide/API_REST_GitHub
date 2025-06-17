import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.routes import users_data
from api.security import get_current_user
import os
from dotenv import load_dotenv
from api.models import User

load_dotenv()

client = TestClient(app)

admin = os.getenv("ADMIN")
password = os.getenv("PASSWD")

# Bypass l'authentification dans tous les tests
app.dependency_overrides[get_current_user] = lambda: "user1"

#creation fausse liste User
@pytest.fixture(autouse=True)
def setup_users():
    users_data.clear()
    users_data.extend([
        User(
            id=1,
            login="user1",
            email="user1@example.com",
            full_name="User One",
            created_at="2024-01-01T00:00:00Z",
            avatar_url="https://example.com/avatar1.png",
            bio="Bio de user1"
        ),
        User(
            id=2,
            login="user2",
            email="user2@example.com",
            full_name="User Two",
            created_at="2024-01-02T00:00:00Z",
            avatar_url="https://example.com/avatar2.png",
            bio="Bio de user2"
        )
    ])


def test_home():
    r = client.get("/")
    assert r.status_code == 200

def test_token_fail():
    r = client.post("/token", data={"username": "u", "password": "bad"})
    assert r.status_code == 401

def test_token_ok():
    r = client.post("/token", data={"username": admin, "password": password})
    assert r.status_code == 200

def test_get_all_users():

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["login"] == "user1"
    assert data[1]["login"] == "user2"
    
def test_get_user_ok():
    r = client.get("/users/user1")
    assert r.status_code == 200
    assert r.json()["login"] == "user1"

def test_get_user_not_found():
    r = client.get("/users/none")
    assert r.status_code == 404

def test_search():
    r = client.get("/users/search?q=user")
    assert r.status_code == 200
    results = r.json()
    assert all("user" in user["login"].lower() for user in results)

def test_protected():
    r = client.get("/protected")
    assert r.status_code == 200
    assert "Bienvenue user1" in r.json()["message"]