from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📦 Купить прокси"), KeyboardButton(text="👤 Мои прокси")],
            [KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )

def get_type_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="IPv4"), KeyboardButton(text="IPv6"), KeyboardButton(text="Mobile")]
        ],
        resize_keyboard=True
    )

def get_country_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Франция"), KeyboardButton(text="Германия"), KeyboardButton(text="США")]
        ],
        resize_keyboard=True
    )

def get_duration_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="1 день"), KeyboardButton(text="7 дней")],
            [KeyboardButton(text="1 месяц"), KeyboardButton(text="3 месяца"), KeyboardButton(text="6 месяцев")]
        ],
        resize_keyboard=True
    )

def get_confirm_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить"), KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )
