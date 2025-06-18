"""
Module FastAPI pour la gestion des routes utilisateur et de l'authentification.

Ce routeur propose :
- Une route d'accueil
- L'accès à la liste des utilisateurs (protégée)
- La recherche d'utilisateurs par login (protégée)
- La consultation détaillée d'un utilisateur (protégée)
- Une route protégée de test
- L'authentification via token JWT

Les routes nécessitent un token valide sauf pour l'accueil et la génération du token.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from .models import User
from .security import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter()
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Stockage temporaire des utilisateurs (en mémoire)
users_data: List[User] = []

@router.get("/", summary="Page d'accueil")
async def root():
    """
    Route publique d'accueil de l'API.

    Returns:
        dict: Message de bienvenue.
    """
    return {"message": "Bienvenue sur l'API utilisateurs"}

@router.get("/users/", response_model=List[User], summary="Liste des utilisateurs")
def get_all_users(current_user: str = Depends(get_current_user)):
    """
    Retourne la liste complète des utilisateurs (protégé par authentification).

    Args:
        current_user (str): Utilisateur courant authentifié (injecté).

    Returns:
        List[User]: Liste des utilisateurs.
    """
    return users_data

@router.get("/users/search", response_model=List[User], summary="Recherche utilisateur")
def search_users(q: str, current_user: str = Depends(get_current_user)):
    """
    Recherche d'utilisateurs par login (insensible à la casse).

    Args:
        q (str): Terme de recherche à filtrer dans les logins.
        current_user (str): Utilisateur authentifié.

    Returns:
        List[User]: Liste des utilisateurs correspondant à la recherche.
    """
    return [user for user in users_data if q.lower() in user.login.lower()]

@router.get("/users/{login}", response_model=User, summary="Détails utilisateur")
def get_user_by_login(login: str, current_user: str = Depends(get_current_user)):
    """
    Retourne les détails d'un utilisateur à partir de son login.

    Args:
        login (str): Nom d'utilisateur GitHub.
        current_user (str): Utilisateur authentifié.

    Returns:
        User: Détail du profil utilisateur.

    Raises:
        HTTPException: Si l'utilisateur n'existe pas.
    """
    for user in users_data:
        if user.login == login:
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@router.get("/protected", summary="Route protégée")
async def protected_route(current_user: str = Depends(get_current_user)):
    """
    Route de test protégée par authentification.

    Args:
        current_user (str): Utilisateur authentifié.

    Returns:
        dict: Message de confirmation d'accès.
    """
    return {"message": f"Bienvenue {current_user}, vous êtes authentifié"}

@router.post("/token", summary="Génère un token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authentifie un utilisateur et génère un token JWT.

    Args:
        form_data (OAuth2PasswordRequestForm): Données du formulaire de login.

    Returns:
        dict: Token d'accès, type de token et durée de validité.

    Raises:
        HTTPException: Si les identifiants sont invalides.
    """
    username = form_data.username
    password = form_data.password
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": username})
    return {
        "access_token": token,
        "token_type": "bearer",
        "duree": f"{access_token_expire_minutes} minutes"
    }
