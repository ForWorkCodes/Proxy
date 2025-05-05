import logging
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN, POSTGRES_DSN

from handlers.start import router as start_router
from handlers.buy_proxy import router as buy_proxy_router
from handlers.settings import router as settings_router
from handlers.profile import router as profile_router
from handlers.checker import router as checker_router
db_pool = None

async def main():
    global db_pool

    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутеры
    dp.include_routers(start_router, buy_proxy_router, settings_router, profile_router, checker_router)

    # Подключение к базе данных
    db_pool = await asyncpg.create_pool(
        dsn=POSTGRES_DSN,
        min_size=5,
        max_size=20
    )
    dp["db_pool"] = db_pool

    # Запуск бота
    print(f"Старт бота")
    try:
        await dp.start_polling(bot)
    finally:
        await db_pool.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
