from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts, get_text
from keyboards.menus import (
    get_main_menu, empty_proxy_menu, download_proxies_keyboard, get_start_menu
)
from services.proxy_api_client import ProxyAPIClient

router = Router()


@router.callback_query(F.data == "my_proxy")
async def my_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    service = ProxyAPIClient()
    response = await service.get_my_list_proxy(callback.from_user.id)
    texts = await get_texts(state)

    if not response.success:
        if response.status_code == 2001:
            empty_menu = await empty_proxy_menu(state)
            await callback.message.answer(text=texts['empty_proxy_text'], reply_markup=empty_menu)
        else:
            keyboard = await get_main_menu(state)
            await callback.message.answer(text=texts['api_error'], reply_markup=keyboard)

    my_proxy_num = len(response.list)
    await callback.message.answer(texts["you_have_proxy_count"] + ": " + str(my_proxy_num))

    if my_proxy_num > 0:
        if my_proxy_num > 10:
            download_menu = await download_proxies_keyboard(state)
            await callback.message.answer(texts['download_proxies'], reply_markup=download_menu)
        else:
            for idx, proxy in enumerate(response.list, start=1):
                country = texts["country_" + proxy.country]
                date_end = proxy.date_end.strftime("%d.%m.%Y %H:%M") if proxy.date_end else "—"
                proxy_text = (
                    f"<b>IP: </b>{proxy.host}:{proxy.port}\n"
                    f"<b>{texts['type']}: </b>{proxy.type.upper()}\n"
                    f"<b>{texts['version']}: </b>{proxy.version}\n"
                    f"<b>{texts['country']}: </b>{country}\n"
                    f"<b>{texts['time_to']}: </b>{date_end}"
                )
                await callback.message.answer(proxy_text, parse_mode="HTML")

            menu = await get_main_menu(state)
            await callback.message.answer(text=texts['menu_title'], reply_markup=menu)


@router.callback_query(F.data == "test_add_proxy")
async def test_add_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    data = await state.get_data()
    current_proxy = data.get("user", {}).get("my_proxy", 0)
    data["user"]["my_proxy"] = current_proxy + 4
    await state.update_data(data)

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Тестовое прокси добавлено")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "download_proxies_csv")
async def download_proxies_csv(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()

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
    await callback.message.delete()

    service = ProxyAPIClient()
    response = await service.get_link_my_proxy(callback.from_user.id, "xls")

    if not response["success"]:
        await callback.message.answer(text=texts["Error"])
    else:
        await callback.message.answer_document(response["file_url"])

    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


