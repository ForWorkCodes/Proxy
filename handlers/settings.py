from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.user_service import update_user_language
from keyboards.menus import (
    get_settings_menu, get_language_menu, get_main_menu,
    get_notifications_menu, get_menu_sms_notification
)
from asyncpg import Pool

router = Router()

@router.callback_query(F.data == "my_settings")
async def my_settings(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Настройки", reply_markup=get_settings_menu())

@router.callback_query(F.data == "change_language")
async def change_language(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Выберите язык", reply_markup=get_language_menu())

@router.callback_query(F.data == "change_language_ru")
async def change_language_ru(callback: CallbackQuery, db_pool: Pool) -> None:
    await update_user_language(callback.from_user.id, "ru", db_pool)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Язык успешно изменен")
    await callback.message.answer(text="Главное меню:", reply_markup=get_main_menu())

@router.callback_query(F.data == "change_language_en")
async def change_language_en(callback: CallbackQuery, db_pool: Pool) -> None:
    await update_user_language(callback.from_user.id, "en", db_pool)
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Язык успешно изменен")
    await callback.message.answer(text="Главное меню:", reply_markup=get_main_menu())

@router.callback_query(F.data == "change_notifications")
async def change_notifications(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Уведомления", reply_markup=get_notifications_menu())

@router.callback_query(F.data == "menu_sms_notification")
async def menu_sms_notification(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Смс о продлении", reply_markup=get_menu_sms_notification())

@router.callback_query(F.data == "enable_sms_notification")
async def enable_sms_notification(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Смс о продлении включены")
    await callback.message.answer(text="Главное меню:", reply_markup=get_main_menu())

@router.callback_query(F.data == "disable_sms_notification")
async def disable_sms_notification(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(text="Смс о продлении выключены")
    await callback.message.answer(text="Главное меню:", reply_markup=get_main_menu())
