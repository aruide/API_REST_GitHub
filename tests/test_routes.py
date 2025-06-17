"""
Tests automatisés de l'API GitHub Users avec FastAPI et Pytest

Ce fichier couvre les principales fonctionnalités de l'API, notamment :

Authentification :
---------------------
- Génération de token invalide (mauvais identifiants)
- Génération de token valide avec credentials du .env

Utilisateurs :
-----------------
- Récupération de tous les utilisateurs (/users/)
- Récupération d’un utilisateur spécifique (/users/{login})
- Gestion des utilisateurs inexistants (404)
- Recherche d’utilisateurs via query (/users/search?q=...)

Routes protégées :
---------------------
- Accès à la route /protected pour un utilisateur authentifié

Setup des tests :
--------------------
- TestClient utilisé pour simuler les appels API
- Auth désactivée via override de `get_current_user`
- Préchargement d'une fausse base utilisateur avec un `pytest.fixture(autouse=True)`

À lancer avec :
------------------
pytest tests/test_routes.py

Remarque : nécessite un fichier `.env` valide contenant `ADMIN` et `PASSWD`.
"""

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

# Désactivation de l'authentification réelle pour les tests
app.dependency_overrides[get_current_user] = lambda: "user1"

# Création automatique d'une fausse liste d'utilisateurs pour tous les tests
@pytest.fixture(autouse=True)
def setup_users():
    """
    Fixture exécutée avant chaque test : initialise une liste de deux utilisateurs.
    """
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
    """Test de la page d'accueil (GET /)"""
    r = client.get("/")
    assert r.status_code == 200


def test_token_fail():
    """Test de génération de token avec identifiants invalides"""
    r = client.post("/token", data={"username": "u", "password": "bad"})
    assert r.status_code == 401


def test_token_ok():
    """Test de génération de token avec identifiants valides"""
    r = client.post("/token", data={"username": admin, "password": password})
    assert r.status_code == 200


def test_get_all_users():
    """Test de récupération de tous les utilisateurs (GET /users/)"""
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["login"] == "user1"
    assert data[1]["login"] == "user2"
    

def test_get_user_ok():
    """Test de récupération d'un utilisateur existant (GET /users/{login})"""
    r = client.get("/users/user1")
    assert r.status_code == 200
    assert r.json()["login"] == "user1"


def test_get_user_not_found():
    """Test de récupération d'un utilisateur inexistant (404 attendu)"""
    r = client.get("/users/none")
    assert r.status_code == 404


def test_search():
    """Test de la recherche d'utilisateurs par login (GET /users/search?q=...)"""
    r = client.get("/users/search?q=user")
    assert r.status_code == 200
    results = r.json()
    assert all("user" in user["login"].lower() for user in results)


def test_protected():
    """Test d'accès à la route protégée (GET /protected)"""
    r = client.get("/protected")
    assert r.status_code == 200
    assert "Bienvenue user1" in r.json()["message"]
