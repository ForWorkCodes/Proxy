from aiogram import Dispatcher, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states.buy_proxy import BuyProxyStates
from keyboards.menus import get_type_kb, get_country_kb, get_duration_kb, get_confirm_kb, get_main_menu

async def buy_proxy_start(message: types.Message):
    await message.answer("Выберите тип прокси:", reply_markup=get_type_kb())
    await BuyProxyStates.ChoosingType.set()

async def choose_type(message: types.Message, state: FSMContext):
    print("choose_type")
    await state.update_data(proxy_type=message.text)
    await message.answer("Выберите страну:", reply_markup=get_country_kb())
    await BuyProxyStates.ChoosingCountry.set()

async def choose_duration(message: types.Message, state: FSMContext):
    print("choose_duration")
    await state.update_data(country=message.text)
    await message.answer("На какой срок:", reply_markup=get_duration_kb())
    await BuyProxyStates.ChoosingDuration.set()

async def choose_quantity(message: types.Message, state: FSMContext):
    print("choose_quantity")
    await state.update_data(duration=message.text)
    await message.answer("Введите количество прокси:", reply_markup=ReplyKeyboardRemove())
    await BuyProxyStates.ChoosingQuantity.set()

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
    await BuyProxyStates.Confirming.set()

async def choose_confirm(message: types.Message, state: FSMContext):
    print("choose_confirm")
    await message.answer("Ваш заказ принят в обработку. Спасибо:", reply_markup=get_main_menu())
    await state.finish()

async def choose_cancel(message: types.Message, state: FSMContext):
    await message.answer("Заказ отменён.", reply_markup=get_main_menu())
    await state.finish()

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(buy_proxy_start, lambda m: m.text == "📦 Купить прокси", state='*')
    dp.register_message_handler(choose_type, state=BuyProxyStates.ChoosingType)
    dp.register_message_handler(choose_duration, state=BuyProxyStates.ChoosingCountry)
    dp.register_message_handler(choose_quantity, state=BuyProxyStates.ChoosingDuration)
    dp.register_message_handler(choose_confirming, state=BuyProxyStates.ChoosingQuantity)
    dp.register_message_handler(choose_confirm, lambda m: m.text == "✅ Подтвердить", state=BuyProxyStates.Confirming)
    dp.register_message_handler(choose_cancel, lambda m: m.text == "❌ Отмена", state=BuyProxyStates.Confirming)
