import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.buy_proxy import router as buy_proxy_router
from handlers.settings import router as settings_router
from handlers.profile import router as profile_router
from handlers.checker import router as checker_router
from handlers.my_proxy import router as my_proxy_router
from middlewares.user_loader import UserLoaderMiddleware


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_routers(start_router, buy_proxy_router, settings_router, profile_router, checker_router, my_proxy_router)

    # Подключаем middleware
    dp.message.middleware(UserLoaderMiddleware())
    dp.callback_query.middleware(UserLoaderMiddleware())

    # Запуск бота
    print(f"Старт бота")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
