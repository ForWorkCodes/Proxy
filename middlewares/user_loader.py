from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message, CallbackQuery
from services.user_service import create_user

class UserLoaderMiddleware(BaseMiddleware):
    def __init__(self):
        print("middleware")

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        state = data['state']
        message = event.message if isinstance(event, CallbackQuery) else event
        await create_user(message, state)
        return await handler(event, data)