from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from utils.telegram import safe_delete_message
from keyboards.menus import (
    get_main_menu, empty_proxy_menu, download_proxies_keyboard, proxy_checker_list
)
from services.proxy_api_client import ProxyAPIClient
from dtos.proxy_dto import ProxyItem
from states.proxy import CancelProxy

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
                f"<b>{texts['login']}: </b>{proxy.login_proxy}\n"
                f"<b>{texts['password']}: </b>{proxy.pass_proxy}\n"
                f"<b>{texts['time_to']}: </b>{date_end}\n"
                f"<b>{texts['is_prolog']}: </b>{texts['Yes'] if proxy.auto_prolong else texts['No']}"
            )
            await callback.message.answer(proxy_text, parse_mode="HTML")

    await callback.message.answer(text=text, reply_markup=empty_menu)


@router.callback_query(F.data == "cancel_proxy")
async def cancel_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CancelProxy.Choose)
    texts = await get_texts(state)
    await callback.answer()
    await safe_delete_message(callback)

    service = ProxyAPIClient()
    response = await service.get_my_list_proxy(callback.from_user.id)

    if not response.success:
        await state.update_data(proxy_list=[])
        await state.set_state(None)

        if response.status_code == 2001:
            empty_menu = await empty_proxy_menu(state)
            await callback.message.answer(text=texts['empty_proxy_text'], reply_markup=empty_menu)
        else:
            keyboard = await get_main_menu(state)
            await callback.message.answer(text=texts['api_error'], reply_markup=keyboard)

        return

    proxy_list_raw = [proxy.model_dump() for proxy in response.list]
    await state.update_data(proxy_list=proxy_list_raw)

    if not proxy_list_raw:
        await state.set_state(None)
        empty_menu = await empty_proxy_menu(state)
        await callback.message.answer(text=texts['empty_proxy_text'], reply_markup=empty_menu)
        return

    visible_proxies = response.list[:20]
    keyboard = await proxy_checker_list(state, visible_proxies)

    await callback.message.answer(text=texts['choose_proxy_to_cancel'], reply_markup=keyboard)


@router.message(CancelProxy.Choose)
async def cancel_proxy_choose(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    texts = await get_texts(state)
    proxy_list_raw = data.get("proxy_list", [])
    proxy_list = [ProxyItem(**p) for p in proxy_list_raw]
    visible_proxies = proxy_list[:20]
    keyboard = await proxy_checker_list(state, visible_proxies)

    main_menu_text = texts["main_menu_btn"]
    selected = message.text.strip()

    if selected == main_menu_text:
        keyboard = await get_main_menu(state)
        await state.set_state(None)
        await message.answer(texts["menu_title"], reply_markup=keyboard)
        return

    selected_proxy = None
    for proxy_data in proxy_list_raw:
        ip_port = f"{proxy_data['host']}:{proxy_data['port']}"
        if selected == ip_port:
            selected_proxy = proxy_data
            break

    if not selected_proxy:
        await message.answer(text=texts["wrong_message"], reply_markup=keyboard)
        return

    proxy_api_client = ProxyAPIClient()
    response = await proxy_api_client.delete_proxy(message.from_user.id, selected)

    if response.get("success"):
        updated_proxy_list = [
            proxy for proxy in proxy_list_raw
            if f"{proxy['host']}:{proxy['port']}" != selected
        ]
        await state.update_data(proxy_list=updated_proxy_list)

        success_text = texts["proxy_deleted"].format(proxy=selected)
        await message.answer(text=success_text)

        if not updated_proxy_list:
            await state.set_state(None)
            keyboard = await get_main_menu(state)
            await message.answer(text=texts["menu_title"], reply_markup=keyboard)
            return

        proxy_list = [ProxyItem(**p) for p in updated_proxy_list]
        visible_proxies = proxy_list[:20]
        keyboard = await proxy_checker_list(state, visible_proxies)
    else:
        error_text = response.get("error") or texts["proxy_delete_failed"]
        await message.answer(text=error_text)

    await message.answer(text=texts["choose_proxy_to_cancel"], reply_markup=keyboard)


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


