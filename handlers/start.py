from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.menus import get_main_menu, get_start_menu
from utils.i18n import resolve_language
from services.user_service import get_or_create_user
from asyncpg import Pool

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, db_pool: Pool) -> None:
    lang = await get_or_create_user(message, db_pool)
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>", reply_markup=get_main_menu()  )

@router.message()
async def fallback(message: Message, db_pool: Pool) -> None:
    lang = await get_or_create_user(message, db_pool)
    await message.answer("Я не понимаю. Выберите пункт из меню.", reply_markup=get_start_menu())