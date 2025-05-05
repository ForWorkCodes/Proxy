from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from data.locales import get_texts, get_text
from keyboards.menus import (
    get_main_menu, empty_proxy_menu, download_proxies_keyboard
)

router = Router()

@router.callback_query(F.data == "my_proxy")
async def my_proxy(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    data = await state.get_data()
    my_proxy = data.get("user", {}).get("my_proxy", 0)

    await callback.answer()
    await callback.message.delete()

    await callback.message.answer("У тебя есть прокси в количестве: " + str(my_proxy))

    if (my_proxy > 0):
        if (my_proxy > 10):
            download_menu = await download_proxies_keyboard(state)
            await callback.message.answer(texts['download_proxies'], reply_markup=download_menu)
        else:
            for i in range(my_proxy):
                proxy_text = await get_text(state, "proxy:")
                await callback.message.answer(text=proxy_text + str(i + 1))
            empty_menu = await empty_proxy_menu(state)
            await callback.message.answer(text=texts['proxy:'], reply_markup=empty_menu)
    else:
        empty_menu = await empty_proxy_menu(state)
        await callback.message.answer(text=texts['empty_proxy_text'], reply_markup=empty_menu)

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
    await callback.message.answer(text="Скачано")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)

@router.callback_query(F.data == "download_proxies_xls")
async def download_proxies_xls(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Скачано")
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


