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
        "current_balance": "Текущий баланс",
        "spb": "СПБ",
        "crypto": "Крипта",
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
        "select_proxy_type": "Выберите версию прокси:",
        "select_proxy_httptype": "Выберите тип прокси:",
        "select_country": "Выберите страну:",
        "enter_proxy_quantity": "Введите количество прокси:",
        "available_proceed_payment": "Есть в наличии. Перейти к оплате?",
        "deducting_from_balance": "Списываю с баланса...",
        "purchase_success": "Успешная покупка",
        "purchase_cancelled": "Покупка отменена.",
        "no_choose": "❗ Пока ничего не выбрано",
        "choose": "Выбери",
        "test_add_proxy": "Тестовое добавление прокси",
        "buy_proxy?": "Купить прокси?",
        "empty_proxy_text": "У вас нет прокси",
        "you_have_proxy_count": "У тебя есть прокси в количестве",
        "download_proxies": "Скачать",
        "proxy_type_not_selected": "proxy_type не задан. Сначала выберите версию прокси.",
        "proxy_type_not_selected_error": "proxy_type должен быть установлен перед выбором страны",
        "wrong_quantity": "❌ Введите корректное количество (целое число больше нуля).",
        "not_enough_proxies": "Недостаточно прокси в выбранной стране. Доступно",
        "proxy_not_available": "Такой прокси недоступен, просим прощения за неудобства",
        "api_error": "❗ Ошибка при подключении к серверу. Попробуйте позже",
        "no_money_purshare?": "Недостаточно денег на счету, пополнить?",
        "error_days": "Указано неправильное количество дней",
        "Error": "Ошибка",
        "time_to": "Срок до",
        "your_choice": "Ваш выбор",
        "Yes, pay": "Да, оплатить",
        "Cancel": "Отмена",
        "link_pay": "Для оплаты перейдите по ссылке",
        "back": "🔙 Назад",
        "select_period_days:": "Выберите количество дней (от 1 до 180)",
        "proxy_is_not_active": "Прокси не активно",
        "proxy_is_active": "Прокси активно",
        "rub_symbol": "₽",
        "proxy:": "Прокси:",
        "country_ru": "Россия",
        "country_ua": "Украина",
        "country_us": "США",
        "country_gb": "Великобритания",
        "country_de": "Германия",
        "country_ca": "Канада",
        "country_nl": "Нидерланды",
        "country_fr": "Франция",
        "country_jp": "Япония",
        "country_it": "Италия",
        "country_pl": "Польша",
        "country_es": "Испания",
        "country_ch": "Швейцария",
        "country_se": "Швеция",
        "country_ro": "Румыния",
        "country_cz": "Чехия",
        "country_bg": "Болгария",
        "country_lt": "Литва",
        "country_lv": "Латвия",
        "country_sk": "Словакия",
        "country_fi": "Финляндия",
        "country_be": "Бельгия",
        "country_no": "Норвегия",
        "country_hu": "Венгрия",
        "country_gr": "Греция",
        "country_il": "Израиль",
        "country_ie": "Ирландия",
        "country_pt": "Португалия",
        "country_dk": "Дания",
        "country_si": "Словения",
        "country_hr": "Хорватия",
        "country_lu": "Люксембург",
        "country_md": "Молдова",
        "country_by": "Беларусь",
        "country_ee": "Эстония",
        "country_rs": "Сербия",
        "country_tr": "Турция",
        "country_ae": "ОАЭ",
        "country_in": "Индия",
        "country_ng": "Нигерия",
        "country_id": "Индонезия",
        "country_th": "Таиланд",
        "country_vn": "Вьетнам",
        "country_sg": "Сингапур",
        "country_my": "Малайзия",
        "country_hk": "Гонконг",
        "country_za": "ЮАР",
        "country_br": "Бразилия",
        "country_ar": "Аргентина",
        "country_cl": "Чили",
        "country_au": "Австралия",
        "country_kz": "Казахстан",
        "country_ge": "Грузия",
        "country_tw": "Тайвань",
        "country_cy": "Кипр",
        "country_mx": "Мексика",
        "country_sa": "Саудовская Аравия",
        "country_eg": "Египет",
        "country_pk": "Пакистан",
        "country_bd": "Бангладеш",
        "country_ph": "Филиппины",
        "country_ma": "Марокко",
        "country_tn": "Тунис",
        "country_al": "Албания",
        "country_is": "Исландия",
        "country_mt": "Мальта",
        "country_mc": "Монако",
        "country_li": "Лихтенштейн",
        "country_kr": "Южная Корея",
        "country_sc": "Сейшелы",
        "country_kg": "Киргизия",
        "country_at": "Австрия",
        "country_tj": "Таджикистан",
        "country_am": "Армения",
        "country_tm": "Туркменистан",
        "country_uz": "Узбекистан",
        "country_cn": "Китай",
        "version": "Версия",
        "type": "Тип",
        "country": "Страна",
        "quantity": "Кол-во",
        "days": "Дней",
        "price": "Цена",
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
        "current_balance": "Current balance",
        "spb": "SPB",
        "crypto": "Crypto",
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
        "select_proxy_type": "Select proxy version:",
        "select_proxy_httptype": "Select proxy type:",
        "select_country": "Select country:",
        "enter_proxy_quantity": "Enter number of proxies:",
        "available_proceed_payment": "Available. Proceed to payment?",
        "deducting_from_balance": "Deducting from balance...",
        "purchase_success": "Successful purchase",
        "purchase_cancelled": "Purchase cancelled.",
        "no_choose": "❗ Nothing selected yet",
        "choose": "Choose",
        "test_add_proxy": "Test add proxy",
        "buy_proxy?": "Buy proxy?",
        "empty_proxy_text": "You have no proxies",
        "you_have_proxy_count": "You have proxies in the amount of",
        "download_proxies": "Download",
        "proxy_type_not_selected": "proxy_type not selected. First select proxy type.",
        "proxy_type_not_selected_error": "proxy_type must be set before selecting a country",
        "wrong_quantity": "❌ Enter a valid quantity (a positive integer).",
        "your_choice": "Your choice",
        "Cancel": "Cancel",
        "Yes, pay": "Yes, pay",
        "link_pay": "To pay, follow the link",
        "back": "🔙 Back",
        "not_enough_proxies": "Not enough proxies in the selected country. Available",
        "proxy_not_available": "This proxy is unavailable, sorry for the inconvenience",
        "api_error": "❗ Error connecting to the server. Try again later",
        "no_money": "Not enough money in the account",
        "error_days": "Incorrect number of days specified",
        "time_to": "Deadline until",
        "Error": "Error",
        "select_period_days:": "Select the number of days (from 1 to 180)",
        "proxy_is_not_active": "Proxy is not active",
        "proxy_is_active": "Proxy is active",
        "rub_symbol": "₽",
        "proxy:": "Proxy:",
        "country_ru": "Russia",
        "country_ua": "Ukraine",
        "country_us": "United States",
        "country_gb": "United Kingdom",
        "country_de": "Germany",
        "country_ca": "Canada",
        "country_nl": "Netherlands",
        "country_fr": "France",
        "country_jp": "Japan",
        "country_it": "Italy",
        "country_pl": "Poland",
        "country_es": "Spain",
        "country_ch": "Switzerland",
        "country_se": "Sweden",
        "country_ro": "Romania",
        "country_cz": "Czech Republic",
        "country_bg": "Bulgaria",
        "country_lt": "Lithuania",
        "country_lv": "Latvia",
        "country_sk": "Slovakia",
        "country_fi": "Finland",
        "country_be": "Belgium",
        "country_no": "Norway",
        "country_hu": "Hungary",
        "country_gr": "Greece",
        "country_il": "Israel",
        "country_ie": "Ireland",
        "country_pt": "Portugal",
        "country_dk": "Denmark",
        "country_si": "Slovenia",
        "country_hr": "Croatia",
        "country_lu": "Luxembourg",
        "country_md": "Moldova",
        "country_by": "Belarus",
        "country_ee": "Estonia",
        "country_rs": "Serbia",
        "country_tr": "Turkey",
        "country_ae": "UAE",
        "country_in": "India",
        "country_ng": "Nigeria",
        "country_id": "Indonesia",
        "country_th": "Thailand",
        "country_vn": "Vietnam",
        "country_sg": "Singapore",
        "country_my": "Malaysia",
        "country_hk": "Hong Kong",
        "country_za": "South Africa",
        "country_br": "Brazil",
        "country_ar": "Argentina",
        "country_cl": "Chile",
        "country_au": "Australia",
        "country_kz": "Kazakhstan",
        "country_ge": "Georgia",
        "country_tw": "Taiwan",
        "country_cy": "Cyprus",
        "country_mx": "Mexico",
        "country_sa": "Saudi Arabia",
        "country_eg": "Egypt",
        "country_pk": "Pakistan",
        "country_bd": "Bangladesh",
        "country_ph": "Philippines",
        "country_ma": "Morocco",
        "country_tn": "Tunisia",
        "country_al": "Albania",
        "country_is": "Iceland",
        "country_mt": "Malta",
        "country_mc": "Monaco",
        "country_li": "Liechtenstein",
        "country_kr": "South Korea",
        "country_sc": "Seychelles",
        "country_kg": "Kyrgyzstan",
        "country_at": "Austria",
        "country_tj": "Tajikistan",
        "country_am": "Armenia",
        "country_tm": "Turkmenistan",
        "country_uz": "Uzbekistan",
        "country_cn": "China",
        "version": "Version",
        "type": "Type",
        "country": "Country",
        "quantity": "Quantity",
        "days": "Days",
        "price": "Price",
    }
}

DEFAULT_LANG = "en"

async def get_texts(state: FSMContext) -> dict:
    data = await state.get_data()
    lang = data.get("user", {}).get("language", DEFAULT_LANG)
    return texts.get(lang, texts[DEFAULT_LANG])

async def get_text(state: FSMContext, key: str) -> str:
    texts = await get_texts(state)
    return texts[key]
