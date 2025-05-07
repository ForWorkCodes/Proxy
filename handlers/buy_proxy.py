from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.buy_proxy import BuyProxy
from data.locales import get_text, get_texts
from keyboards.menus import (
    proxy_type_keyboard, get_countries_list_keyboard,
    confirm_quantity_keyboard, payment_method_keyboard
)
from itertools import islice

def chunked(iterable, n):
    it = iter(iterable)
    return iter(lambda: list(islice(it, n)), [])

router = Router()

@router.callback_query(F.data == "buy_proxy")
async def buy_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BuyProxy.Type)
    text = await get_text(state, 'select_proxy_type')
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=proxy_type_keyboard())

@router.callback_query(BuyProxy.Type, F.data.startswith("type_"))
async def select_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(proxy_type=callback.data.split("_")[1])
    await state.set_state(BuyProxy.Country)

    await callback.answer()
    await callback.message.delete()

    text = await get_text(state, 'select_country')
    keyboard = await get_countries_list_keyboard(state)
    await callback.message.answer(text, reply_markup=keyboard)

@router.message(BuyProxy.Country)
async def select_country(message: Message, state: FSMContext):
    print(message.text)
    await state.update_data(country=message.text)
    await state.set_state(BuyProxy.Quantity)
    text = await get_text(state, 'enter_proxy_quantity')
    await message.answer(text)

@router.message(BuyProxy.Quantity)
async def select_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    # Здесь можно вставить проверку наличия
    await state.set_state(BuyProxy.ConfirmAvailability)
    text = await get_text(state, 'available_proceed_payment')

    summary = await get_proxy_summary(state)
    await message.answer(f"{text}\n\n<b>Ваш выбор:</b>\n{summary}")

    await message.answer(text, reply_markup=confirm_quantity_keyboard())

@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_yes")
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyProxy.PaymentChoice)
    text = await get_text(state, 'select_payment_method')

    summary = await get_proxy_summary(state)
    await callback.message.answer(f"{text}\n\n<b>Ваш выбор:</b>\n{summary}")

    await callback.message.answer(text, reply_markup=payment_method_keyboard())
    await callback.answer()

@router.callback_query(BuyProxy.PaymentChoice, F.data == "pay_balance")
async def pay_with_balance(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyProxy.PaymentProcess)
    text_processing = await get_text(state, 'deducting_from_balance')
    await callback.message.answer(text_processing)

    # Здесь должна быть логика оплаты
    await state.set_state(BuyProxy.ProxyDelivery)
    text_delivered = await get_text(state, 'proxy_delivered')
    await callback.message.answer(text_delivered)
    await callback.answer()

@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_cancel")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = await get_text(state, 'purchase_cancelled')
    await callback.message.answer(text)
    await callback.answer()

async def get_proxy_summary(state: FSMContext) -> str:
    data = await state.get_data()
    lines = []

    if "proxy_type" in data:
        lines.append(f"🌐 Тип: <b>{data['proxy_type']}</b>")
    if "country" in data:
        lines.append(f"🏳️ Страна: <b>{data['country']}</b>")
    if "quantity" in data:
        lines.append(f"🔢 Кол-во: <b>{data['quantity']}</b>")

    if not lines:
        return "❗ Пока ничего не выбрано."
    return "\n".join(lines)