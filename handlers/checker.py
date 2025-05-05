from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from keyboards.menus import (
    get_main_menu
)

router = Router()

@router.callback_query(F.data == "checker")
async def checker(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    checker_text = "Заглушка для отображения чекера"
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=checker_text)
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)