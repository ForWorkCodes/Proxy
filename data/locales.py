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
        "(is_on)": "(Включено)",
        "(is_off)": "(Выключено)",
        "sms_renewal": "Смс о продлении",
        "sms_enabled": "Смс о продлении включены",
        "sms_disabled": "Смс о продлении выключены",
        "select_proxy_type": "Выберите версию прокси:",
        "select_proxy_httptype": "Выберите тип прокси:",
        "select_country": "Выберите страну:",
        "enter_proxy_quantity": "Введите количество прокси:",
        "1_min_quant": "дня минимум",
        "2_min_quant": "дней минимум",
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
        "how_choose_proxy": "Как выбрать?",
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
        "is_prolog": "Автопродление",
        "your_choice": "Ваш выбор",
        "Yes, pay": "Да, оплатить",
        "Yes, pay (prolog)": "Да, оплатить (с автопродлением)",
        "Cancel": "Отмена",
        "link_pay": "Для оплаты перейдите по ссылке",
        "back": "🔙 Назад",
        "select_period_days": "Выберите количество дней",
        "proxy_is_not_active": "Прокси не активно",
        "proxy_is_active": "Прокси активно",
        "rub_symbol": "₽",
        "usd_symbol": "$",
        "notification_proxy_expiring": "Данный прокси скоро закончиться",
        "proxy:": "Прокси:",
        "login": "Логин",
        "password": "Пароль",
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
        "how_choose_proxy_text": (
            "<b>Как выбрать прокси</b>\n\n"
            "<b>IPv6</b>\n"
            "• Подходят только для сайтов с поддержкой IPv6.\n"
            "• Обычно дешевле, чем IPv4.\n"
            "• Выдаются в одни руки.\n\n"
            "<b>IPv4</b>\n"
            "• Подходят для всех сайтов и сервисов.\n"
            "• Универсальный и надёжный вариант.\n"
            "• Выдаются в одни руки.\n\n"
            "<b>IPv4 Shared</b>\n"
            "• Подходят для всех сайтов.\n"
            "• Один IP делят до 3 человек.\n"
            "• Дешевле, но возможны ограничения при высокой нагрузке."
        ),
        "faq_text": (
            "1. <b>Как купить</b> → Выберите страну и тип прокси, оплатите прямо в боте, доступ придет сразу.\n\n"
            "2. <b>Что лучше выбрать: IPv4 или IPv6</b> → IPv4 стабильнее и подходит для большинства сервисов, "
            "IPv6 дешевле и отлично работает там, где он поддерживается. Уточнять стоит на сервисе, который требует прокси.\n\n"
            "3. <b>На сколько выдается прокси</b> → Минимальный срок — 30 дней. Можно продлить в пару кликов.\n\n"
            "4. <b>Как продлить</b> → В разделе “Мои прокси” нажмите “Продлить”, выберите срок и оплатите.\n\n"
            "5. <b>Можно ли поменять страну</b> → Да, но только купив новый прокси. Обмен не предусмотрен.\n\n"
            "6. <b>Что делать, если прокси не работает</b> → Проверьте логин/пароль и настройки. Если ошибка повторяется — пишите в поддержку.\n\n"
            "7. <b>Сколько можно использовать на одном устройстве</b> → Один прокси можно подключить к неограниченному количеству устройств/ПО, "
            "параллельные подключения не гарантируются.\n\n"
            "8. <b>Анонимность</b> → Прокси полностью скрывает ваш реальный IP, но ответственность за действия несет пользователь.\n\n"
            "9. <b>Оплата</b> → Принимаем крипту. Все автоматизировано.\n\n"
            "10. <b>Вы даёте замену</b> → Да, если прокси “умирает” раньше срока, мы бесплатно заменим."
        ),
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
        "(is_on)": "(On)",
        "(is_off)": "(Off)",
        "sms_renewal": "SMS Renewal Notifications",
        "sms_enabled": "SMS renewal notifications enabled",
        "sms_disabled": "SMS renewal notifications disabled",
        "select_proxy_type": "Select proxy version:",
        "select_proxy_httptype": "Select proxy type:",
        "select_country": "Select country:",
        "enter_proxy_quantity": "Enter number of proxies:",
        "1_min_quant": "days minimum",
        "2_min_quant": "days minimum",
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
        "how_choose_proxy": "How to choose?",
        "proxy_type_not_selected": "proxy_type not selected. First select proxy type.",
        "proxy_type_not_selected_error": "proxy_type must be set before selecting a country",
        "wrong_quantity": "❌ Enter a valid quantity (a positive integer).",
        "your_choice": "Your choice",
        "Cancel": "Cancel",
        "Yes, pay": "Yes, pay",
        "Yes, pay (prolog)": "Yes, pay (with auto-renewal)",
        "link_pay": "To pay, follow the link",
        "back": "🔙 Back",
        "not_enough_proxies": "Not enough proxies in the selected country. Available",
        "proxy_not_available": "This proxy is unavailable, sorry for the inconvenience",
        "api_error": "❗ Error connecting to the server. Try again later",
        "no_money": "Not enough money in the account",
        "error_days": "Incorrect number of days specified",
        "time_to": "Deadline until",
        "is_prolog": "Auto-renewal",
        "Error": "Error",
        "select_period_days": "Select the number of days",
        "proxy_is_not_active": "Proxy is not active",
        "proxy_is_active": "Proxy is active",
        "rub_symbol": "₽",
        "usd_symbol": "$",
        "notification_proxy_expiring": "This proxy will expire soon",
        "proxy:": "Proxy:",
        "login": "Login",
        "password": "Password",
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
        "how_choose_proxy_text": (
            "<b>How to choose a proxy</b>\n\n"
            "<b>IPv6</b>\n"
            "• Suitable only for websites that support IPv6.\n"
            "• Usually cheaper than IPv4.\n"
            "• Issued individually (not shared).\n\n"
            "<b>IPv4</b>\n"
            "• Works with all websites and services.\n"
            "• A reliable and universal option.\n"
            "• Issued individually (not shared).\n\n"
            "<b>IPv4 Shared</b>\n"
            "• Works with all websites.\n"
            "• One IP address is shared by up to 3 people.\n"
            "• Cheaper, but may have limitations under heavy use."
        ),
        "faq_text": (
            "1. <b>How to buy</b> → Choose the country and proxy type, pay directly in the bot, and access will be provided instantly.\n\n"
            "2. <b>Which is better: IPv4 or IPv6</b> → IPv4 is more stable and works for most services, "
            "IPv6 is cheaper and works perfectly where supported. Always check the service that requires the proxy.\n\n"
            "3. <b>Proxy validity</b> → Minimum period is 30 days. You can extend it in just a few clicks.\n\n"
            "4. <b>How to renew</b> → In the “My Proxies” section, click “Renew”, choose the period and pay.\n\n"
            "5. <b>Can I change the country</b> → Yes, but only by purchasing a new proxy. Exchange is not provided.\n\n"
            "6. <b>What to do if the proxy doesn’t work</b> → Check your login/password and settings. If the issue repeats, contact support.\n\n"
            "7. <b>How many devices can I use it on</b> → One proxy can be connected to an unlimited number of devices/apps, "
            "but simultaneous parallel connections are not guaranteed.\n\n"
            "8. <b>Anonymity</b> → Proxies fully hide your real IP, but responsibility for actions lies with the user.\n\n"
            "9. <b>Payment</b> → We accept crypto. Everything is automated.\n\n"
            "10. <b>Do you provide replacements</b> → Yes, if a proxy “dies” before its expiration date, we will replace it for free."
        ),
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


def get_text_by_land(lang: str):
    return texts.get(lang, texts[DEFAULT_LANG])
