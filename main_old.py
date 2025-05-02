from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from dotenv import load_dotenv
import os

# Загрузка токена
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

# Настройка бота и хранилища FSM
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# FSM-состояния
class BuyProxyStates(StatesGroup):
    ChoosingType = State()
    ChoosingCountry = State()
    ChoosingDuration = State()
    ChoosingQuantity = State()
    Confirming = State()

def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📦 Купить прокси"), KeyboardButton("👤 Мой профиль"))
    kb.add(KeyboardButton("⚙️ Настройки"))
    return kb

# Старт
@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Привет! Что вы хотите сделать?", reply_markup=get_main_menu())

# === Купить прокси ===

@dp.message_handler(lambda m: m.text == "📦 Купить прокси", state='*')
async def buy_proxy_start(message: types.Message, state: FSMContext):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("IPv4"), KeyboardButton("IPv6"), KeyboardButton("Mobile"))
    await message.answer("Выберите тип прокси:", reply_markup=kb)
    await BuyProxyStates.ChoosingType.set()

@dp.message_handler(state=BuyProxyStates.ChoosingType)
async def choose_type(message: types.Message, state: FSMContext):
    await state.update_data(proxy_type=message.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Украина"), KeyboardButton("Германия"), KeyboardButton("США"))
    await message.answer("Выберите страну:", reply_markup=kb)
    await BuyProxyStates.ChoosingCountry.set()

@dp.message_handler(state=BuyProxyStates.ChoosingCountry)
async def choose_country(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("1 день"), KeyboardButton("7 дней"), KeyboardButton("30 дней"))
    await message.answer("Выберите срок:", reply_markup=kb)
    await BuyProxyStates.ChoosingDuration.set()

@dp.message_handler(state=BuyProxyStates.ChoosingDuration)
async def choose_duration(message: types.Message, state: FSMContext):
    await state.update_data(duration=message.text)
    await message.answer("Введите количество прокси:", reply_markup=ReplyKeyboardRemove())
    await BuyProxyStates.ChoosingQuantity.set()

@dp.message_handler(state=BuyProxyStates.ChoosingQuantity)
async def choose_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число.")
        return
    await state.update_data(quantity=int(message.text))
    data = await state.get_data()

    summary = (
        f"Вы выбрали:\n"
        f"Тип: {data['proxy_type']}\n"
        f"Страна: {data['country']}\n"
        f"Срок: {data['duration']}\n"
        f"Количество: {data['quantity']}\n\n"
        f"Подтвердить заказ?"
    )
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("✅ Подтвердить"), KeyboardButton("❌ Отмена"))
    await message.answer(summary, reply_markup=kb)
    await BuyProxyStates.Confirming.set()

@dp.message_handler(lambda m: m.text == "✅ Подтвердить", state=BuyProxyStates.Confirming)
async def confirm_order(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer("Ваш заказ принят в обработку. Спасибо!", reply_markup=get_main_menu())
    await state.finish()

@dp.message_handler(lambda m: m.text == "❌ Отмена", state=BuyProxyStates.Confirming)
async def cancel_order(message: types.Message, state: FSMContext):
    await message.answer("Операция отменена.", reply_markup=get_main_menu())
    await state.finish()

# Фолбэк — любое сообщение
@dp.message_handler(state='*')
async def fallback(message: types.Message):
    await message.answer("Пожалуйста, выберите действие из меню.", reply_markup=get_main_menu())

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
