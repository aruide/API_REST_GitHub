"""
Tests unitaires du module d'authentification JWT (FastAPI)

Ce fichier utilise `pytest` pour tester les fonctionnalités du module `api.security`, notamment :
- l'authentification via identifiants (`authenticate_user`)
- la génération de tokens JWT (`create_access_token`)
- la validation et extraction d'utilisateur depuis un token (`get_current_user`)

Les identifiants de test sont chargés depuis le fichier `.env` via les variables :
- ADMIN : nom d'utilisateur
- PASSWD : mot de passe

Fonctions testées :
-------------------
- test_authenticate_user_valid : cas d'authentification valide
- test_authenticate_user_invalid_user : utilisateur inexistant
- test_authenticate_user_invalid_password : mot de passe incorrect
- test_create_access_token_and_decode : création et décodage JWT
- test_get_current_user_valid_token : extraction correcte de l'utilisateur depuis un token valide
- test_get_current_user_invalid_token : rejet d’un token JWT invalide

À lancer avec :
---------------
    pytest tests/test_auth.py

Assurez-vous que le fichier `.env` est présent et correctement configuré avant de lancer les tests.
"""

import pytest
from datetime import timedelta
from fastapi import HTTPException
from jose import jwt
import os
from dotenv import load_dotenv
from api.security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    USERS,
    secret_key,
    algorithm,
)

# Chargement des variables d'environnement
load_dotenv()

# Utilisateur fictif (doit correspondre à ceux du fichier .env)
admin = os.getenv("ADMIN")
password = os.getenv("PASSWD")

def test_authenticate_user_valid():
    assert authenticate_user(admin, password) is True

def test_authenticate_user_invalid_user():
    assert authenticate_user("invalid_user", "password") is False

def test_authenticate_user_invalid_password():
    assert authenticate_user(admin, "wrong_password") is False

def test_create_access_token_and_decode():
    data = {"sub": admin}
    token = create_access_token(data, timedelta(minutes=5))
    decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
    assert decoded["sub"] == admin
    assert "exp" in decoded

def test_get_current_user_valid_token():
    token = create_access_token({"sub": admin}, timedelta(minutes=5))
    result = get_current_user(token)
    assert result == admin

def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        get_current_user("invalid.token.value")
    assert exc_info.value.status_code == 401
    assert "invalide" in exc_info.value.detail.lower()
