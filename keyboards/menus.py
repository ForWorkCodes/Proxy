from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from data.locales import get_texts, get_text
from services.proxy_api_client import ProxyAPIClient
from aiogram.exceptions import TelegramBadRequest
from dtos.proxy_dto import ProxyItem


async def make_back_keyboard(state: FSMContext) -> ReplyKeyboardMarkup:
    texts = await get_texts(state)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts["back"])]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def get_start_menu(state: FSMContext):
    main_menu_text = await get_text(state, 'main_menu_btn')
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=main_menu_text)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def get_main_menu(state: FSMContext):
    data = await state.get_data()
    new_data = {}
    if "user" in data:
        new_data["user"] = data["user"]
    await state.set_data(new_data)
    await state.set_state(None)

    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts['buy_proxy'], callback_data="buy_proxy")],
        [InlineKeyboardButton(text=texts['my_proxy'], callback_data="my_proxy")],
        [InlineKeyboardButton(text=texts['balance'], callback_data="my_balance")],
        [InlineKeyboardButton(text=texts['checker'], callback_data="checker")],
        [InlineKeyboardButton(text=texts['settings'], callback_data="my_settings")],
    ])


# Клавиатура для настроек
async def get_settings_menu(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts['language'], callback_data="change_language")],
        [InlineKeyboardButton(text=texts['notifications'], callback_data="change_notifications")],
        [InlineKeyboardButton(text=texts['back'], callback_data="main_menu_btn")],
    ])


def get_language_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="change_language_ru")],
        [InlineKeyboardButton(text="English", callback_data="change_language_en")]
    ])


async def get_notifications_menu(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["sms_renewal"], callback_data="menu_sms_notification")]
    ])


async def get_menu_sms_notification(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["Yes"], callback_data="enable_sms_notification")],
        [InlineKeyboardButton(text=texts["No"], callback_data="disable_sms_notification")]
    ])


# Клавиатура для баланса
async def get_balance_menu(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["top_up_balance"], callback_data="top_up_balance_menu")],
        [InlineKeyboardButton(text=texts["back"], callback_data="main_menu_btn")],
    ])


async def get_top_up_balance_menu(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        #[InlineKeyboardButton(text=texts["spb"], callback_data="spb_top_up")],
        [InlineKeyboardButton(text=texts["crypto"], callback_data="crypto_top_up")],
        [InlineKeyboardButton(text=texts["back"], callback_data="main_menu_btn")],
    ])


# Клавиатура для моих прокси
async def empty_proxy_menu(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["buy_proxy?"], callback_data="buy_proxy")],
        [InlineKeyboardButton(text=texts["back"], callback_data="main_menu_btn")]
    ])


async def download_proxies_keyboard(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=".csv", callback_data="download_proxies_csv")],
        [InlineKeyboardButton(text=".xls", callback_data="download_proxies_xls")],
        [InlineKeyboardButton(text=texts["back"], callback_data="main_menu_btn")],
    ])


# Клавиатуры для выбора типа прокси
async def proxy_type_keyboard(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="IPv6", callback_data="type_ipv6")],
        [InlineKeyboardButton(text="IPv4", callback_data="type_ipv4")],
        [InlineKeyboardButton(text="IPv4 Shared", callback_data="type_ipv4shared")],
        [InlineKeyboardButton(text=texts["back"], callback_data="type_back")],
    ])


async def proxy_httptype_keyboard(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="SOCKS", callback_data="httptype_socks")],
        [InlineKeyboardButton(text="HTTP", callback_data="httptype_http")],
        [InlineKeyboardButton(text=texts["back"], callback_data="httptype_back")],
    ])


async def get_countries_list_keyboard(state: FSMContext):
    country_service = ProxyAPIClient()
    data = await state.get_data()
    texts = await get_texts(state)

    proxy_version = data.get("proxy_version")
    if not proxy_version:
        raise TelegramBadRequest(texts["proxy_type_not_selected"])

    country_codes = await country_service.get_countries(proxy_version)

    if not country_codes:
        return None
    
    keyboard = []
    row = []

    for code in country_codes:
        country_name = await country_service.get_country_name(state, code)
        row.append(KeyboardButton(text=country_name))
        if len(row) == 3:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([KeyboardButton(text=texts["back"])])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def get_quantity_keyboard(state: FSMContext):
    texts = await get_texts(state)
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=texts["back"])]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


async def confirm_proxy_keyboard(state: FSMContext):
    texts = await get_texts(state)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=texts["Yes, pay"], callback_data="pay_yes")],
        [InlineKeyboardButton(text=texts["Cancel"], callback_data="pay_cancel")],
    ])


async def proxy_checker_list(state: FSMContext, proxy_list: list[ProxyItem]):
    columns = 2
    buttons = []
    for proxy in proxy_list:
        text = f"{proxy.host}:{proxy.port}"
        buttons.append(KeyboardButton(text=text))

    keyboard = []
    for i in range(0, len(buttons), columns):
        keyboard.append(buttons[i:i + columns])

    main_menu_text = await get_text(state, 'main_menu_btn')
    keyboard.append([KeyboardButton(text=main_menu_text)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True)


async def top_up_amount_list(state: FSMContext):
    texts = await get_texts(state)

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="100 " + texts["rub_symbol"], callback_data="amount_100.0"),
            InlineKeyboardButton(text="200 " + texts["rub_symbol"], callback_data="amount_200.0")
        ],
        [
            InlineKeyboardButton(text="400 " + texts["rub_symbol"], callback_data="amount_400.0"),
            InlineKeyboardButton(text="500 " + texts["rub_symbol"], callback_data="amount_500.0")
        ],
        [
            InlineKeyboardButton(text="1000 " + texts["rub_symbol"], callback_data="amount_1000.0"),
            InlineKeyboardButton(text="1500 " + texts["rub_symbol"], callback_data="amount_1500.0")
        ],
        [
            InlineKeyboardButton(text="2000 " + texts["rub_symbol"], callback_data="amount_2000.0"),
            InlineKeyboardButton(text=texts["back"], callback_data="amount_back")
        ]
    ])
