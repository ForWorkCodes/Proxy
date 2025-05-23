from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from services import UserService
from keyboards.menus import (
    get_balance_menu, get_top_up_balance_menu, get_main_menu
)

router = Router()

@router.callback_query(F.data == "my_balance")
async def my_balance(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    balance_menu = await get_balance_menu(state)

    user_service = UserService()
    user = await user_service.get_balance(callback.from_user.id)

    if not user["success"]:
        balance_text = texts["api_error"]
    else:
        balance_text = texts["current_balance"] + ": " + str(user["balance"]) + " " + user["currency"]

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=balance_text)
    await callback.message.answer(text=texts['menu'], reply_markup=balance_menu)

@router.callback_query(F.data == "top_up_balance_menu")
async def top_up_balance_menu(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    top_up_balance_menu = await get_top_up_balance_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts['choose'], reply_markup=top_up_balance_menu)

@router.callback_query(F.data == "spb_top_up")
async def spb_top_up(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Заглушка для оплаты в СПБ")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)

@router.callback_query(F.data == "krypto_top_up")
async def krypto_top_up(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Заглушка для оплаты в крипте")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)