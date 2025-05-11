from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from states.buy_proxy import BuyProxy
from data.locales import get_text, get_texts
from keyboards.menus import (
    proxy_type_keyboard, get_countries_list_keyboard,
    confirm_quantity_keyboard, payment_method_keyboard, get_main_menu,
    get_quantity_keyboard, make_back_keyboard
)
from itertools import islice
from services.country_service import CountryService


def chunked(iterable, n):
    it = iter(iterable)
    return iter(lambda: list(islice(it, n)), [])

router = Router()

@router.callback_query(F.data == "buy_proxy")
async def buy_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BuyProxy.Type)
    text = await get_text(state, 'select_proxy_type')
    proxy_type_menu = await proxy_type_keyboard(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text, reply_markup=proxy_type_menu)

@router.callback_query(BuyProxy.Type, F.data.startswith("type_"))
async def select_type(callback: CallbackQuery, state: FSMContext):
    if callback.data == "type_back":
        await state.clear()
        await callback.answer()
        await callback.message.delete()
        text = await get_text(state, 'main_menu_btn')
        main_menu = await get_main_menu(state)
        await callback.message.answer(text, reply_markup=main_menu)
        return
    
    await state.update_data(proxy_type=callback.data.split("_")[1])
    await state.set_state(BuyProxy.Country)

    await callback.answer()
    await callback.message.delete()

    text = await get_text(state, 'select_country')
    keyboard = await get_countries_list_keyboard(state)

    if not keyboard:
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await callback.message.answer(f"{error_text}", reply_markup=back_keyboard)
        return

    await callback.message.answer(text, reply_markup=keyboard)

@router.message(BuyProxy.Country)
async def select_country(message: Message, state: FSMContext):
    if message.text == await get_text(state, 'back'):
        await state.set_state(BuyProxy.Type)
        await message.delete()
        text = await get_text(state, 'select_proxy_type')
        proxy_type_menu = await proxy_type_keyboard(state)
        await message.answer(text, reply_markup=proxy_type_menu)
        return
    
    country_service = CountryService()
    country_dict = await country_service.get_country_dict(state)

    # Найти код страны по вводу пользователя
    selected_country_code = None
    for code, name in country_dict.items():
        if name.lower() == message.text.lower():
            selected_country_code = code
            break

    if not selected_country_code:
        # Страна не найдена — сообщаем и повторно показываем клавиатуру
        warning_text = await get_text(state, 'wrong_message')
        retry_text = await get_text(state, 'select_country')
        keyboard = await get_countries_list_keyboard(state)

        await message.answer(f"{warning_text}\n\n{retry_text}", reply_markup=keyboard)
        return

    await state.update_data(country=selected_country_code)
    await state.set_state(BuyProxy.Quantity)

    text = await get_text(state, 'enter_proxy_quantity')
    quantity_keyboard = await get_quantity_keyboard(state)
    await message.answer(text, reply_markup=quantity_keyboard)

@router.message(BuyProxy.Quantity)
async def select_quantity(message: Message, state: FSMContext):
    if message.text == await get_text(state, 'back'):
        await state.set_state(BuyProxy.Country)
        await message.delete()
        text = await get_text(state, 'select_country')
        keyboard = await get_countries_list_keyboard(state)
        await message.answer(text, reply_markup=keyboard)
        return
        
    quantity_str = message.text.strip()

    # Проверяем, что это число и > 0
    if not quantity_str.isdigit() or int(quantity_str) <= 0:
        error_text = await get_text(state, 'wrong_quantity')
        retry_text = await get_text(state, 'enter_proxy_quantity')
        await message.answer(f"{error_text}\n\n{retry_text}")
        return

    quantity = int(quantity_str)
    data = await state.get_data()
    country_code = data.get("country")
    proxy_type = data.get("proxy_type")
    
    service = CountryService()
    is_available, available_quantity, success = await service.check_availability(proxy_type, country_code, quantity)

    if not success:
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(error_text, reply_markup=back_keyboard)
        return

    if not is_available:
        not_available_text = await get_text(state, 'not_enough_proxies')
        retry_text = await get_text(state, 'enter_proxy_quantity')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(
            f"{not_available_text} :{available_quantity}\n\n{retry_text}",
            reply_markup=back_keyboard
        )
        return

    await state.update_data(quantity=quantity)
    await state.set_state(BuyProxy.ConfirmAvailability)

    text = await get_text(state, 'available_proceed_payment')
    summary = await get_proxy_summary(state)

    await message.answer(f"{text}\n\n<b>{await get_text(state, 'your_choice')}:</b>\n{summary}")
    await message.answer(text, reply_markup=confirm_quantity_keyboard())

@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_yes")
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyProxy.PaymentChoice)
    text = await get_text(state, 'select_payment_method')

    summary = await get_proxy_summary(state)
    await callback.message.answer(f"{text}\n\n<b>{await get_text(state, 'your_choice')}:</b>\n{summary}")

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