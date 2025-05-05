from aiogram.fsm.context import FSMContext

texts = {
    "ru": {
        "Yes": "Да",
        "No": "Нет",
        "menu": "Меню:",
        "menu_title": "Главное меню:",
        "main_menu_btn": "Главное меню",
        "settings": "Настройки",
        "balance": "Баланс",
        "top_up_balance": "Пополнить баланс",
        "spb": "СПБ",
        "krypto": "Крипта",
        "my_proxy": "Мои прокси",
        "buy_proxy": "Купить прокси",
        "checker": "Чекер",
        "language": "Язык",
        "notifications": "Уведомления",
        "first_hello": "Привет",
        "wrong_message": "Я не понимаю. Выберите пункт из меню.",
        "language_changed": "Язык успешно изменен",
        "choose_language": "Выберите язык",
        "notifications_title": "Уведомления",
        "sms_renewal": "Смс о продлении",
        "sms_enabled": "Смс о продлении включены",
        "sms_disabled": "Смс о продлении выключены",
        "select_proxy_type": "Выберите тип прокси:",
        "select_country": "Выберите страну:",
        "enter_proxy_quantity": "Введите количество прокси:",
        "available_proceed_payment": "Есть в наличии. Перейти к оплате?",
        "select_payment_method": "Выберите способ оплаты:",
        "deducting_from_balance": "Списываю с баланса...",
        "proxy_delivered": "Прокси выданы:\nIP:PORT:USER:PASS",
        "purchase_cancelled": "Покупка отменена.",
        "choose": "Выбери",
        "test_add_proxy": "Тестовое добавление прокси",
        "buy_proxy?": "Купить прокси?",
        "empty_proxy_text": "У вас нет прокси",
        "download_proxies": "Скачать",
        "proxy:": "Прокси:"
    },
    "en": {
        "Yes": "Yes",
        "No": "No",
        "menu": "Menu:",
        "menu_title": "Main menu:",
        "main_menu_btn": "Main menu",
        "settings": "Settings",
        "balance": "Balance",
        "top_up_balance": "Top up balance",
        "spb": "SPB",
        "krypto": "Krypto",
        "my_proxy": "My Proxies",
        "buy_proxy": "Buy Proxy",
        "checker": "Checker",
        "language": "Language",
        "notifications": "Notifications",
        "first_hello": "Hello",
        "wrong_message": "I don't understand. Select an item from the menu.",
        "language_changed": "Language changed successfully",
        "choose_language": "Choose language",
        "notifications_title": "Notifications",
        "sms_renewal": "SMS Renewal Notifications",
        "sms_enabled": "SMS renewal notifications enabled",
        "sms_disabled": "SMS renewal notifications disabled",
        "select_proxy_type": "Select proxy type:",
        "select_country": "Select country:",
        "enter_proxy_quantity": "Enter number of proxies:",
        "available_proceed_payment": "Available. Proceed to payment?",
        "select_payment_method": "Select payment method:",
        "deducting_from_balance": "Deducting from balance...",
        "proxy_delivered": "Proxies delivered:\nIP:PORT:USER:PASS",
        "purchase_cancelled": "Purchase cancelled.",
        "choose": "Choose",
        "test_add_proxy": "Test add proxy",
        "buy_proxy?": "Buy proxy?",
        "empty_proxy_text": "You have no proxies",
        "download_proxies": "Download",
        "proxy:": "Proxy:"
    }
}

DEFAULT_LANG = "en"

async def get_texts(state: FSMContext) -> dict:
    data = await state.get_data()
    lang = data.get("user", {}).get("lang", DEFAULT_LANG)
    return texts.get(lang, texts[DEFAULT_LANG])

async def get_text(state: FSMContext, key: str) -> str:
    texts = await get_texts(state)
    return texts[key]
