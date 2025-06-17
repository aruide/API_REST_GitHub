from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    login: str
    id: int
    created_at: str
    avatar_url: str
    bio: Optional[str]