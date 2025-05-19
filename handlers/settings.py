from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from services.user_service import update_user_language
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
    await callback.message.delete()
    await callback.message.answer(text=texts['settings'], reply_markup=settings_menu)


@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery, state: FSMContext) -> None:
    text = await get_text(state, 'choose_language')
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=get_language_menu())


@router.callback_query(F.data == "change_language_ru")
async def change_language_ru(callback: CallbackQuery, state: FSMContext) -> None:
    await update_user_language(callback.from_user.id, "ru", state)
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts['language_changed'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "change_language_en")
async def change_language_en(callback: CallbackQuery, state: FSMContext) -> None:
    await update_user_language(callback.from_user.id, "en", state)
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts['language_changed'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "change_notifications")
async def change_notifications(callback: CallbackQuery, state: FSMContext) -> None:
    text = await get_text(state, 'notifications_title')
    notifications_menu = await get_notifications_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=notifications_menu)


@router.callback_query(F.data == "menu_sms_notification")
async def menu_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    text = await get_text(state, 'sms_renewal')
    menu_sms_notification = await get_menu_sms_notification(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=menu_sms_notification)


@router.callback_query(F.data == "enable_sms_notification")
async def enable_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts['sms_enabled'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)


@router.callback_query(F.data == "disable_sms_notification")
async def disable_sms_notification(callback: CallbackQuery, state: FSMContext) -> None:
    texts = await get_texts(state)
    main_menu = await get_main_menu(state)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text=texts['sms_disabled'])
    await callback.message.answer(text=texts['menu_title'], reply_markup=main_menu)
