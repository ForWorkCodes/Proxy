from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.buy_proxy import BuyProxyStates
from keyboards.menus import get_type_kb, get_country_kb, get_duration_kb, get_confirm_kb, get_main_menu

router = Router()

@router.message(F.text == "📦 Купить прокси")
async def buy_proxy_start(message: types.Message, state: FSMContext):
    await message.answer("Выберите тип прокси:", reply_markup=get_type_kb())
    await state.set_state(BuyProxyStates.ChoosingType)

@router.message(BuyProxyStates.ChoosingType)
async def choose_type(message: types.Message, state: FSMContext):
    print("choose_type")
    await state.update_data(proxy_type=message.text)
    await message.answer("Выберите страну:", reply_markup=get_country_kb())
    await state.set_state(BuyProxyStates.ChoosingCountry)

@router.message(BuyProxyStates.ChoosingCountry)
async def choose_duration(message: types.Message, state: FSMContext):
    print("choose_duration")
    await state.update_data(country=message.text)
    await message.answer("На какой срок:", reply_markup=get_duration_kb())
    await state.set_state(BuyProxyStates.ChoosingDuration)

@router.message(BuyProxyStates.ChoosingDuration)
async def choose_quantity(message: types.Message, state: FSMContext):
    print("choose_quantity")
    await state.update_data(duration=message.text)
    await message.answer("Введите количество прокси:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(BuyProxyStates.ChoosingQuantity)

@router.message(BuyProxyStates.ChoosingQuantity)
async def choose_confirming(message: types.Message, state: FSMContext):
    print("choose_confirming")
    await state.update_data(quantity=message.text)
    data = await state.get_data()

    summary = (
        f"Вы выбрали:\n"
        f"Тип: {data['proxy_type']}\n"
        f"Страна: {data['country']}\n"
        f"Срок: {data['duration']}\n"
        f"Количество: {data['quantity']}\n\n"
        f"Подтвердить заказ?"
    )
    await message.answer(summary, reply_markup=get_confirm_kb())
    await state.set_state(BuyProxyStates.Confirming)

@router.message(BuyProxyStates.Confirming, F.text == "✅ Подтвердить")
async def choose_confirm(message: types.Message, state: FSMContext):
    print("choose_confirm")
    await message.answer("Ваш заказ принят в обработку. Спасибо:", reply_markup=get_main_menu())
    await state.clear()

@router.message(BuyProxyStates.Confirming, F.text == "❌ Отмена")
async def choose_cancel(message: types.Message, state: FSMContext):
    await message.answer("Заказ отменён.", reply_markup=get_main_menu())
    await state.clear()
