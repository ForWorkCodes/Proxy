from aiohttp import ClientSession, ClientError
from config import API_BASE_URL
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class UserServiceAPI:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def get_user(self, telegram_id: int) -> Optional[dict]:
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.base_url}/users/by-telegram-id/{telegram_id}") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except ClientError as e:
            logger.error(f"API error in get_user: {e}")
            return None

    async def upsert_user(self, telegram_id: int, chat_id: int, username: Optional[str],
                          first_name: Optional[str], language: str) -> Optional[dict]:
        payload = {
            "telegram_id": str(telegram_id),
            "chat_id": str(chat_id),
            "username": username,
            "firstname": first_name,
            "language": language,
        }

        try:
            async with ClientSession() as session:
                async with session.post(f"{self.base_url}/users/upsert", json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except ClientError as e:
            logger.error(f"API error in upsert_user: {e}")
            return None

    async def update_language(self, telegram_id: int, lang: str):
        try:
            async with ClientSession() as session:
                await session.patch(
                    f"{self.base_url}/users/{telegram_id}/language",
                    json={"language": lang}
                )
        except ClientError as e:
            logger.error(f"API error in update_language: {e}")
