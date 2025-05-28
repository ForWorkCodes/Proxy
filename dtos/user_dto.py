from pydantic import BaseModel
from typing import Optional


class UserUpsertDTO(BaseModel):
    telegram_id: str
    chat_id: str
    username: Optional[str]
    firstname: Optional[str]
    language: str
    active: bool
    notification: bool
