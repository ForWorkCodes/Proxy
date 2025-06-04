from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from utils.telegram import safe_delete_message
from services import UserService, ProxyAPIClient
from states.proxy import TopUp
from keyboards.menus import (
    get_balance_menu, get_top_up_balance_menu, get_main_menu, top_up_amount_list
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
    await safe_delete_message(callback)
    await callback.message.answer(text=balance_text)
    await callback.message.answer(text=texts['menu'], reply_markup=balance_menu)


@router.callback_query(F.data == "top_up_balance_menu")
async def top_up_balance_menu(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    topup_balance_menu = await get_top_up_balance_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=texts['choose'], reply_markup=topup_balance_menu)


@router.callback_query(F.data == "spb_top_up")
async def spb_top_up(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text="Заглушка для оплаты в СПБ")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "crypto_top_up")
async def krypto_top_up(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)

    await callback.answer()
    await safe_delete_message(callback)

    await state.set_state(TopUp.TypeTopUp)
    await state.update_data(provider="cryptocloud")

    menu = await top_up_amount_list(state)
    await callback.message.answer(text=texts['choose'], reply_markup=menu)


@router.callback_query(TopUp.TypeTopUp, F.data.startswith("amount_"))
async def select_amount(callback: CallbackQuery, state: FSMContext):
    texts = await get_texts(state)

    await callback.answer()
    await safe_delete_message(callback)

    if callback.data == "amount_back":
        await state.clear()
        topup_balance_menu = await get_top_up_balance_menu(state)
        await callback.message.answer(text=texts['choose'], reply_markup=topup_balance_menu)
        return

    data = await state.get_data()
    provider = data.get("provider")
    amount = float(callback.data.split("_")[1])
    await state.update_data(amount=amount)

    service = ProxyAPIClient()
    response = await service.get_link_topup(callback.from_user.id, provider, amount)

    if not response["success"]:
        await callback.message.answer(response["error"])
    else:
        link = response["topup_url"]
        if link:
            await callback.message.answer(f"{texts['link_pay']} ({amount} {texts['rub_symbol']}): {link}")
        else:
            await callback.message.answer(texts['Error'])

    main_menu = await get_main_menu(state)
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)
