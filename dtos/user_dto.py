from pydantic import BaseModel
from typing import Optional


class UserUpsertDTO(BaseModel):
    telegram_id: int
    chat_id: int
    username: Optional[str]
    firstname: Optional[str]
    language: str
