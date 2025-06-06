from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from utils.telegram import safe_delete_message
from keyboards.menus import (
    get_main_menu, empty_proxy_menu, download_proxies_keyboard
)
from services.proxy_api_client import ProxyAPIClient

router = Router()


@router.callback_query(F.data == "my_proxy")
async def my_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await safe_delete_message(callback)
    service = ProxyAPIClient()
    response = await service.get_my_list_proxy(callback.from_user.id)
    texts = await get_texts(state)
    empty_menu = await empty_proxy_menu(state)
    text = texts['my_proxy']

    if not response.success:
        if response.status_code == 2001:
            text = texts['empty_proxy_text']

        else:
            text = texts['api_error']

    my_proxy_num = len(response.list)
    await callback.message.answer(texts["you_have_proxy_count"] + ": " + str(my_proxy_num))

    if my_proxy_num > 0:
        download_menu = await download_proxies_keyboard(state)
        empty_menu.inline_keyboard = download_menu.inline_keyboard + empty_menu.inline_keyboard

        for idx, proxy in enumerate(response.list, start=1):
            country = texts["country_" + proxy.country]
            date_end = proxy.date_end.strftime("%d.%m.%Y %H:%M") if proxy.date_end else "—"
            proxy_text = (
                f"<b>IP: </b>{proxy.host}:{proxy.port}\n"
                f"<b>{texts['type']}: </b>{proxy.type.upper()}\n"
                f"<b>{texts['version']}: </b>{proxy.version}\n"
                f"<b>{texts['country']}: </b>{country}\n"
                f"<b>{texts['time_to']}: </b>{date_end}\n"
                f"<b>{texts['is_prolog']}: </b>{texts['Yes'] if proxy.auto_prolong else texts['No']}"
            )
            await callback.message.answer(proxy_text, parse_mode="HTML")

    await callback.message.answer(text=text, reply_markup=empty_menu)


@router.callback_query(F.data == "test_add_proxy")
async def test_add_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    data = await state.get_data()
    current_proxy = data.get("user", {}).get("my_proxy", 0)
    data["user"]["my_proxy"] = current_proxy + 4
    await state.update_data(data)

    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer("Тестовое прокси добавлено")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "download_proxies_csv")
async def download_proxies_csv(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)

    service = ProxyAPIClient()
    response = await service.get_link_my_proxy(callback.from_user.id, "csv")

    if not response["success"]:
        await callback.message.answer(text=texts["Error"])
    else:
        print(response["file_url"])
        await callback.message.answer_document(response["file_url"])

    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "download_proxies_xls")
async def download_proxies_xls(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)

    service = ProxyAPIClient()
    response = await service.get_link_my_proxy(callback.from_user.id, "xls")

    if not response["success"]:
        await callback.message.answer(text=texts["Error"])
    else:
        await callback.message.answer_document(response["file_url"])

    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


