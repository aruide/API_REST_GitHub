from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from models import User
from security import authenticate_user, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Stockage temporaire des utilisateurs (à adapter selon ta logique)
users_data: List[User] = []

@router.get("/", summary="Page d'accueil")
async def root():
    return {"message": f"Bienvenue sur l'API utilisateurs"}

@router.get("/users/", response_model=List[User], summary="Liste des utilisateurs")
def get_all_users(current_user: str = Depends(get_current_user)):
    return users_data

@router.get("/users/{login}", response_model=User, summary="Détails utilisateur")
def get_user_by_login(login: str, current_user: str = Depends(get_current_user)):
    for user in users_data:
        if user.login == login:
            return user
    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@router.get("/users/search", response_model=List[User], summary="Recherche utilisateur")
def search_users(q: str, current_user: str = Depends(get_current_user)):
    return [user for user in users_data if q.lower() in user.login.lower()]

@router.post("/token", summary="Génère un token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if not authenticate_user(username, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protected", summary="Route protégée")
async def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Bienvenue {current_user}, vous êtes authentifié"}
