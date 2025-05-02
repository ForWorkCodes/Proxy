from aiogram import Router, types, F
from aiogram.filters import CommandStart
from keyboards.menus import get_main_menu

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=get_main_menu())

@router.message()
async def fallback(message: types.Message):
    await message.answer("Я не понимаю. Выберите пункт из меню.", reply_markup=get_main_menu())
