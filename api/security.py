"""
Module de gestion de l'authentification avec JWT pour une API FastAPI.

Fonctionnalités :
- Authentification d'utilisateur via OAuth2 + JWT
- Création de tokens d'accès
- Validation de token et récupération de l'utilisateur courant

Les identifiants sont chargés depuis un fichier `.env` pour des raisons de sécurité.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import secrets

# Chargement des variables d'environnement
load_dotenv()

# Paramètres de sécurité
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
secret_key = os.getenv("SECRET_KEY")

# Utilisateurs en mémoire (login: password)
USERS = {
    os.getenv("ADMIN"): os.getenv("PASSWD")
}

# Schéma OAuth2 pour FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str) -> bool:
    """
    Vérifie si un nom d'utilisateur et mot de passe sont valides.

    Args:
        username (str): Nom d'utilisateur fourni.
        password (str): Mot de passe fourni.

    Returns:
        bool: True si les identifiants sont valides, sinon False.
    """
    correct_password = USERS.get(username)
    return bool(correct_password and secrets.compare_digest(password, correct_password))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Génère un token JWT avec une date d'expiration.

    Args:
        data (dict): Données à encoder dans le token (ex. : {"sub": username}).
        expires_delta (timedelta | None): Durée de validité du token.

    Returns:
        str: Token JWT encodé.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    Décode un token JWT et retourne le nom d'utilisateur associé.

    Args:
        token (str): Token JWT fourni via OAuth2.

    Returns:
        str: Nom d'utilisateur si le token est valide.

    Raises:
        HTTPException: Si le token est invalide ou expiré.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None or username not in USERS:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username
