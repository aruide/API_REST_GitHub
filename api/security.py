from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import secrets

load_dotenv()

# Paramètres de sécurité
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
secret_key = os.getenv("SECRET_KEY")

# Utilisateurs en mémoire (login: password)
USERS = {
    os.getenv("ADMIN"): os.getenv("PASSWD")
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(username: str, password: str) -> bool:
    correct_password = USERS.get(username)
    return correct_password and secrets.compare_digest(password, correct_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
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
