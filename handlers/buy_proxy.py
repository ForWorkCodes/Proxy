from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.buy_proxy import BuyProxy
from keyboards.menus import (
    proxy_type_keyboard, confirm_country_keyboard,
    confirm_quantity_keyboard, payment_method_keyboard
)

router = Router()

@router.callback_query(F.data == "buy_proxy")
async def buy_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BuyProxy.Type)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите тип прокси:", reply_markup=proxy_type_keyboard())

@router.callback_query(BuyProxy.Type, F.data.startswith("type_"))
async def select_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(proxy_type=callback.data.split("_")[1])
    await state.set_state(BuyProxy.Country)
    await callback.message.answer("Выберите страну (введите вручную):")
    await callback.answer()

@router.message(BuyProxy.Country)
async def select_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(BuyProxy.Quantity)
    await message.answer("Введите количество прокси:")

@router.message(BuyProxy.Quantity)
async def select_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    # Здесь можно вставить проверку наличия
    await state.set_state(BuyProxy.ConfirmAvailability)
    await message.answer("Есть в наличии. Перейти к оплате?", reply_markup=confirm_quantity_keyboard())

@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_yes")
async def confirm_payment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyProxy.PaymentChoice)
    await callback.message.answer("Выберите способ оплаты:", reply_markup=payment_method_keyboard())
    await callback.answer()

@router.callback_query(BuyProxy.PaymentChoice, F.data == "pay_balance")
async def pay_with_balance(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BuyProxy.PaymentProcess)
    await callback.message.answer("Списываю с баланса...")

    # Здесь должна быть логика оплаты
    await state.set_state(BuyProxy.ProxyDelivery)
    await callback.message.answer("Прокси выданы:\nIP:PORT:USER:PASS")
    await callback.answer()

@router.callback_query(BuyProxy.ConfirmAvailability, F.data == "pay_cancel")
async def cancel_payment(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Покупка отменена.")
    await callback.answer()
