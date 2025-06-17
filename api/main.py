from fastapi import FastAPI
from routes import router, users_data
from models import User
import json
import os

app = FastAPI(title="GitHub Users API", description="API pour gérer les utilisateurs GitHub filtrés", version="1.0")

# Charger les données filtered_users.json une fois au démarrage
data_file = os.path.join(os.path.dirname(__file__), "..", "data", "filtered_users.json")

with open(data_file, "r", encoding="utf-8") as f:
    raw_users = json.load(f)

# Convertir les dicts en objets Pydantic User
users_data.extend([User(**u) for u in raw_users])

# Inclure les routes
app.include_router(router)
