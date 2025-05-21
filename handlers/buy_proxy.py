from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.buy_proxy import BuyProxy
from data.locales import get_text
from dtos.proxy_dto import ProxyAvailabilityDTO, ProxyGetPriceDTO, ProxyProcessBuyingDTO
from keyboards.menus import (
    proxy_type_keyboard, get_countries_list_keyboard,
    confirm_proxy_keyboard, get_main_menu,
    make_back_keyboard, get_balance_menu
)
from itertools import islice
from pydantic import ValidationError
from services.proxy_api_client import ProxyAPIClient
import logging


def chunked(iterable, n):
    it = iter(iterable)
    return iter(lambda: list(islice(it, n)), [])


logger = logging.getLogger(__name__)
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
    
    await state.update_data(proxy_version=callback.data.split("_")[1])
    await state.update_data(proxy_type="socks")
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
    
    country_service = ProxyAPIClient()
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
    back_keyboard = await make_back_keyboard(state)
    await message.answer(text, reply_markup=back_keyboard)


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

    try:
        dto = ProxyAvailabilityDTO(
            telegram_id=message.from_user.id,
            version=data.get("proxy_version"),
            country=data.get("country"),
            quantity=quantity
        )
    except KeyError as e:
        logger.error(f"Missing field: {e}")
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(error_text, reply_markup=back_keyboard)
        return
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        error_text = await get_text(state, 'wrong_quantity')
        await message.answer(error_text)
        return

    service = ProxyAPIClient()
    response = await service.check_availability(dto)

    if not response.success:
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(error_text, reply_markup=back_keyboard)
        return

    if not response.available:
        not_available_text = await get_text(state, 'not_enough_proxies')
        retry_text = await get_text(state, 'enter_proxy_quantity')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(
            f"{not_available_text}: {response.available_quantity}\n\n{retry_text}",
            reply_markup=back_keyboard
        )
        return

    await state.update_data(quantity=quantity)
    await state.set_state(BuyProxy.SelectPeriod)

    text = await get_text(state, 'select_period_days:')
    back_keyboard = await make_back_keyboard(state)
    await message.answer(text, reply_markup=back_keyboard)


@router.message(BuyProxy.SelectPeriod)
async def select_period(message: Message, state: FSMContext):
    if message.text == await get_text(state, 'back'):
        await state.set_state(BuyProxy.Quantity)
        await message.delete()
        text = await get_text(state, 'enter_proxy_quantity')
        keyboard = await make_back_keyboard(state)
        await message.answer(text, reply_markup=keyboard)
        return

    days_str = message.text.strip()
    days = int(days_str)

    if days < 1 or days > 180:
        error_text = await get_text(state, 'Error')
        retry_text = await get_text(state, 'select_period_days:')
        await message.answer(f"{error_text}\n\n{retry_text}")
        return

    await state.update_data(days=days)

    data = await state.get_data()

    try:
        dto = ProxyGetPriceDTO(
            telegram_id=message.from_user.id,
            version=data.get("proxy_version"),
            days=days,
            quantity=data.get("quantity")
        )
    except KeyError as e:
        logger.error(f"Missing field: {e}")
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(error_text, reply_markup=back_keyboard)
        return
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        error_text = await get_text(state, 'wrong_quantity')
        await message.answer(error_text)
        return

    service = ProxyAPIClient()
    response = await service.check_price(dto)

    if not response.success:
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(error_text, reply_markup=back_keyboard)
        return

    if not response.available:
        not_available_text = await get_text(state, 'proxy_not_available')
        retry_text = await get_text(state, 'enter_proxy_quantity')
        back_keyboard = await make_back_keyboard(state)
        await message.answer(
            f"{not_available_text}: \n\n{retry_text}",
            reply_markup=back_keyboard
        )
        return

    await state.update_data(price=response.total_price)

    text = await get_text(state, 'available_proceed_payment')
    summary = await get_proxy_summary(state)

    await state.set_state(BuyProxy.ConfirmAvailability)

    menu = await confirm_proxy_keyboard(state)
    await message.answer(f"<b>{await get_text(state, 'your_choice')}: </b>\n{summary}")
    await message.answer(text, reply_markup=menu)


@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_yes")
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(BuyProxy.PaymentProcess)
    text = await get_text(state, 'deducting_from_balance')
    msg = await callback.message.answer(text)

    service = ProxyAPIClient()
    data = await state.get_data()

    try:
        dto = ProxyProcessBuyingDTO(
            telegram_id=str(callback.from_user.id),
            version=data.get("proxy_version"),
            type=data.get("proxy_type"),
            country=data.get("country"),
            days=data.get("days"),
            quantity=data.get("quantity")
        )
    except KeyError as e:
        logger.error(f"Missing field: {e}")
        error_text = await get_text(state, 'api_error')
        back_keyboard = await make_back_keyboard(state)

        await msg.delete()
        await callback.message.answer(error_text, reply_markup=back_keyboard)
        return
    except ValidationError as e:
        logger.warning(f"Validation failed: {e}")
        error_text = await get_text(state, 'wrong_quantity')

        await msg.delete()
        await callback.message.answer(error_text)
        return

    response = await service.process_buying_proxy(dto)
    await msg.delete()

    if not response.success:
        if response.error_code == 400:
            error_text = await get_text(state, 'no_money_purshare?')
            keyboard = await get_balance_menu(state)
        else:
            error_text = await get_text(state, 'api_error')
            keyboard = await get_main_menu(state)

        await callback.message.answer(error_text, reply_markup=keyboard)
    else:
        text = await get_text(state, 'purchase_success')
        await callback.message.answer(text)

        menu = await get_main_menu(state)
        await callback.message.answer(text, reply_markup=menu)
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

    if "proxy_version" in data:
        lines.append(f"Версия: <b>{data['proxy_version']}</b>")
    if "proxy_type" in data:
        lines.append(f"Тип: <b>{data['proxy_type']}</b>")
    if "country" in data:
        lines.append(f"Страна: <b>{data['country']}</b>")
    if "quantity" in data:
        lines.append(f"Кол-во: <b>{data['quantity']}</b>")
    if "days" in data:
        lines.append(f"Дней: <b>{data['days']}</b>")
    if "price" in data:
        lines.append(f"Цена: <b>{data['price']}</b>")

    if not lines:
        return "❗ Пока ничего не выбрано."
    return "\n".join(lines)
