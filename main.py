from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import BOT_TOKEN
import handlers.start
import handlers.buy_proxy

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

handlers.start.register_handlers(dp)
handlers.buy_proxy.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
