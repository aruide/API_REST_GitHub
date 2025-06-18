"""
Point d'entrée de l'application FastAPI.

Cette application charge des utilisateurs GitHub filtrés à partir d'un fichier JSON
et expose une API REST pour interroger ces utilisateurs, avec authentification JWT.
"""

from fastapi import FastAPI
from .routes import router, users_data
from .models import User
import json
import os

# Instanciation de l'application FastAPI avec titre, description et version
app = FastAPI(
    title="GitHub Users API",
    description="API pour gérer les utilisateurs GitHub filtrés",
    version="1.0"
)

# Détermination du chemin vers le fichier filtered_users.json
data_file = os.path.join(os.path.dirname(__file__), "..", "data", "filtered_users.json")

# Chargement des utilisateurs depuis le fichier JSON (au démarrage de l'app)
with open(data_file, "r", encoding="utf-8") as f:
    raw_users = json.load(f)

# Conversion des dictionnaires JSON en objets Pydantic User
users_data.extend([User(**u) for u in raw_users])

# Inclusion des routes définies dans le routeur principal
app.include_router(router)
