from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from services import UserService
from utils.telegram import safe_delete_message
from data.locales import get_texts, get_text
from keyboards.menus import (
    get_settings_menu, get_language_menu, get_main_menu,
    get_notifications_menu, get_menu_sms_notification
)

router = Router()


@router.callback_query(F.data == "my_settings")
async def my_settings(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    settings_menu = await get_settings_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=texts['settings'], reply_markup=settings_menu)


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery, state: FSMContext) -> None:
    text = await get_text(state, 'choose_language')
    menu = await get_language_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=text, reply_markup=menu)


@router.callback_query(F.data == "change_language_ru")
async def change_language_ru(callback: CallbackQuery, state: FSMContext) -> None:
    user_service = UserService()
    await user_service.update_user_language(callback.from_user.id, "ru", state)
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=texts['language_changed'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "change_language_en")
async def change_language_en(callback: CallbackQuery, state: FSMContext) -> None:
    user_service = UserService()
    await user_service.update_user_language(callback.from_user.id, "en", state)
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=texts['language_changed'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "change_notifications")
async def change_notifications(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    text = texts["notifications_title"]

    data = await state.get_data()
    if data["user"]["notification"]:
        text += " " + texts["(is_on)"]
    else:
        text += " " + texts["(is_off)"]

    notifications_menu = await get_notifications_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=text, reply_markup=notifications_menu)


@router.callback_query(F.data == "menu_sms_notification")
async def menu_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    text = await get_text(state, 'sms_renewal')
    menu_sms_not = await get_menu_sms_notification(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=text, reply_markup=menu_sms_not)


@router.callback_query(F.data == "enable_sms_notification")
async def enable_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)

    user_service = UserService()
    await user_service.update_user_notification(callback.from_user.id, True, state)

    await callback.message.answer(text=texts['sms_enabled'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "disable_sms_notification")
async def disable_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)

    user_service = UserService()
    await user_service.update_user_notification(callback.from_user.id, False, state)

    await callback.message.answer(text=texts['sms_disabled'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "main_menu_btn")
async def main_menu_btn(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await safe_delete_message(callback)
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)
