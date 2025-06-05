from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.menus import get_main_menu, get_start_menu
from data.locales import get_text
from aiogram.filters import StateFilter

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    first_hello = await get_text(state, 'first_hello')
    menu = await get_main_menu(state)
    await message.answer(f"{first_hello}, <b>{message.from_user.full_name}!</b>", reply_markup=menu  )


@router.message(StateFilter(None))
async def main_menu_handler(message: Message, state: FSMContext):
    expected_main_menu_text = await get_text(state, 'main_menu_btn')
    if message.text.strip().lower() == expected_main_menu_text.lower():
        menu = await get_main_menu(state)
        menu_title = await get_text(state, 'menu_title')
        await message.answer(menu_title, reply_markup=menu)
    else:
        wrong_message = await get_text(state, 'wrong_message')
        menu = await get_start_menu(state)
        await message.answer(wrong_message, reply_markup=menu)