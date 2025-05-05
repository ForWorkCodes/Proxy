from aiogram import BaseMiddleware
from asyncpg import Pool
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message, CallbackQuery
from services.user_service import create_user

class UserLoaderMiddleware(BaseMiddleware):
    def __init__(self, db_pool: Pool):
        self.db_pool = db_pool

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        state = data['state']
        message = event.message if isinstance(event, CallbackQuery) else event
        await create_user(message, self.db_pool, state)
        return await handler(event, data)