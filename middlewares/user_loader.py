from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any
from aiogram.types import Message, CallbackQuery
from services import UserService


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
        user_service = UserService()

        if isinstance(event, CallbackQuery):
            user = event.from_user
            message = event.message
        else:
            user = event.from_user
            message = event

        await user_service.create_user(user.id, message, state)

        return await handler(event, data)
