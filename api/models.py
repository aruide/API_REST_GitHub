"""
Définition du modèle de données `User` utilisé pour représenter un utilisateur GitHub.

Ce modèle est utilisé pour la validation, la sérialisation et la documentation automatique
des objets utilisateur à travers l'application.
"""

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    """
    Modèle représentant un utilisateur GitHub.

    Attributs :
        login (str)       : Nom d'utilisateur GitHub.
        id (int)          : Identifiant unique de l'utilisateur.
        created_at (str)  : Date de création du compte (format ISO 8601).
        avatar_url (str)  : URL de l'avatar de l'utilisateur.
        bio (Optional[str]): Biographie de l'utilisateur (peut être nulle).
    """
    login: str
    id: int
    created_at: str
    avatar_url: str
    bio: Optional[str]
