from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.locales import texts

def get_start_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")]
        ],
        resize_keyboard=True
    )

def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить прокси", callback_data="buy_proxy")],
        [InlineKeyboardButton(text="Мои прокси", callback_data="my_proxy")],
        [InlineKeyboardButton(text="Баланс", callback_data="my_balance")],
        [InlineKeyboardButton(text="Чекер", callback_data="checker")],
        [InlineKeyboardButton(text="Настройки", callback_data="my_settings")],
    ])

# Клавиатура для настроек
def get_settings_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Язык", callback_data="change_language")],
        [InlineKeyboardButton(text="Уведомления", callback_data="change_notifications")],
    ])

def get_language_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="change_language_ru")],
        [InlineKeyboardButton(text="English", callback_data="change_language_en")]
    ])

def get_notifications_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Смс о продлении", callback_data="menu_sms_notification")]
    ])

def get_menu_sms_notification():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="enable_sms_notification")],
        [InlineKeyboardButton(text="Нет", callback_data="disable_sms_notification")]
    ])

# Клавиатуры для выбора типа прокси
def proxy_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="IPv4", callback_data="type_ipv4")],
        [InlineKeyboardButton(text="IPv6", callback_data="type_ipv6")],
        [InlineKeyboardButton(text="IPv4 Shared", callback_data="type_shared")],
    ])

def confirm_country_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, подходит", callback_data="country_ok")],
        [InlineKeyboardButton(text="Выбрать другую", callback_data="country_change")],
    ])

def confirm_quantity_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, оплатить", callback_data="pay_yes")],
        [InlineKeyboardButton(text="Отменить", callback_data="pay_cancel")],
    ])

def payment_method_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Списать с баланса", callback_data="pay_balance")],
        [InlineKeyboardButton(text="Другой способ", callback_data="pay_other")],
    ])
