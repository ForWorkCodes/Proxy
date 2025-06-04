from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts
from states.proxy import CheckerProxy
from dtos.proxy_dto import ProxyItem
from services.proxy_api_client import ProxyAPIClient
from utils.telegram import safe_delete_message
from keyboards.menus import (
    get_main_menu, empty_proxy_menu, proxy_checker_list
)

router = Router()


@router.callback_query(F.data == "checker")
async def checker(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(CheckerProxy.Choose)
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

    await state.update_data(proxy_list=[proxy.model_dump() for proxy in response.list])
    keyboard = await proxy_checker_list(state, response.list)

    await callback.message.answer(text=texts['choose'], reply_markup=keyboard)


@router.message(CheckerProxy.Choose)
async def checker_proxy_choose(message: Message, state: FSMContext):
    print("CheckerProxy.Choose")
    data = await state.get_data()
    texts = await get_texts(state)
    proxy_list_raw = data.get("proxy_list", [])
    proxy_list = [ProxyItem(**p) for p in proxy_list_raw]
    keyboard = await proxy_checker_list(state, proxy_list)

    main_menu_text = texts["main_menu_btn"]
    selected = message.text.strip()

    if selected == main_menu_text:
        keyboard = await get_main_menu(state)
        await message.answer(texts["menu_title"], reply_markup=keyboard)
        return

    for proxy_data in proxy_list_raw:
        ip_port = f"{proxy_data['host']}:{proxy_data['port']}"
        if selected == ip_port:
            proxy_api_client = ProxyAPIClient()
            response = await proxy_api_client.check_my_proxy(message.from_user.id, ip_port)

            if not response["success"]:
                text = response["error"]
                keyboard = await get_main_menu(state)
            else:
                if response["proxy_status"]:
                    text = texts["proxy_is_active"] + ": " + ip_port
                else:
                    text = texts["proxy_is_not_active"] + ": " + ip_port

            await message.answer(text=text)

    await message.answer(text=texts["choose"], reply_markup=keyboard)
