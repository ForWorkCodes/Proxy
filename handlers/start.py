from aiogram import Dispatcher, types
from keyboards.menus import get_main_menu

async def fallback(message: types.Message):
    await message.answer("Я не понимаю. Выберите пункт из меню.", reply_markup=get_main_menu())

async def cmd_start(message: types.Message):
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=get_main_menu())

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
