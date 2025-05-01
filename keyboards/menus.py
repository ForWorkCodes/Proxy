from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def get_main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📦 Купить прокси"), KeyboardButton("👤 Мои прокси"))
    kb.add(KeyboardButton("⚙️ Настройки"))
    return kb

def get_type_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("IPv4"), KeyboardButton("IPv6"), KeyboardButton("Mobile")
    )

def get_country_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Франция"), KeyboardButton("Германия"), KeyboardButton("США")
    )

def get_duration_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("1 день"), KeyboardButton("7 дней"), KeyboardButton("1 месяц"), KeyboardButton("3 месяца"), KeyboardButton("6 месяцев")
    )

def get_confirm_kb():
    return ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("✅ Подтвердить"), KeyboardButton("❌ Отмена")
    )
