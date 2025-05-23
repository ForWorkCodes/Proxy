import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram.types import CallbackQuery, Message, User
from aiogram.fsm.context import FSMContext
from handlers.settings import (
    my_settings,
    change_language,
    change_language_ru,
    change_language_en,
    change_notifications,
    menu_sms_notification,
    enable_sms_notification,
    disable_sms_notification
)

@pytest.fixture
def callback_query():
    query = AsyncMock(spec=CallbackQuery)
    query.from_user = User(id=123, is_bot=False, first_name="Test")
    query.message = AsyncMock(spec=Message)
    # Настраиваем асинхронные методы
    query.answer = AsyncMock()
    query.message.delete = AsyncMock()
    query.message.answer = AsyncMock()
    return query

@pytest.fixture
def state():
    state = AsyncMock(spec=FSMContext)
    return state

@pytest.mark.asyncio
async def test_my_settings(callback_query, state):
    # Mock the get_texts and get_settings_menu functions
    with patch('handlers.settings.get_texts', new_callable=AsyncMock) as mock_get_texts, \
         patch('handlers.settings.get_settings_menu', new_callable=AsyncMock) as mock_get_settings_menu:
        
        mock_get_texts.return_value = {'settings': 'Settings text'}
        mock_get_settings_menu.return_value = 'settings_menu'
        
        await my_settings(callback_query, state)
        
        # Verify the callback was answered
        callback_query.answer.assert_called_once()
        # Verify the message was deleted
        callback_query.message.delete.assert_called_once()
        # Verify the new message was sent with correct text and markup
        callback_query.message.answer.assert_called_once_with(
            text='Settings text',
            reply_markup='settings_menu'
        )

@pytest.mark.asyncio
async def test_change_language(callback_query, state):
    with patch('handlers.settings.get_text', new_callable=AsyncMock) as mock_get_text, \
         patch('handlers.settings.get_language_menu') as mock_get_language_menu:
        
        mock_get_text.return_value = 'Choose language'
        mock_get_language_menu.return_value = 'language_menu'
        
        await change_language(callback_query, state)
        
        callback_query.answer.assert_called_once()
        callback_query.message.delete.assert_called_once()
        callback_query.message.answer.assert_called_once_with(
            text='Choose language',
            reply_markup=mock_get_language_menu.return_value
        )

@pytest.mark.asyncio
async def test_change_language_ru(callback_query, state):
    with patch("services.user_service.UserService.update_user_language", new_callable=AsyncMock) as mock_update_language, \
         patch('handlers.settings.get_texts', new_callable=AsyncMock) as mock_get_texts, \
         patch('handlers.settings.get_main_menu', new_callable=AsyncMock) as mock_get_main_menu:
        
        mock_get_texts.return_value = {
            'language_changed': 'Language changed',
            'menu_title': 'Main menu'
        }
        mock_get_main_menu.return_value = 'main_menu'
        
        await change_language_ru(callback_query, state)
        
        # Verify language was updated
        mock_update_language.assert_called_once_with(
            callback_query.from_user.id,
            "ru",
            state
        )
        
        # Verify messages were sent
        assert callback_query.message.answer.call_count == 2
        callback_query.message.answer.assert_any_call(text='Language changed')
        callback_query.message.answer.assert_any_call(
            text='Main menu',
            reply_markup='main_menu'
        )

@pytest.mark.asyncio
async def test_change_language_en(callback_query, state):
    with patch("services.user_service.UserService.update_user_language", new_callable=AsyncMock) as mock_update_language, \
         patch('handlers.settings.get_texts', new_callable=AsyncMock) as mock_get_texts, \
         patch('handlers.settings.get_main_menu', new_callable=AsyncMock) as mock_get_main_menu:
        
        mock_get_texts.return_value = {
            'language_changed': 'Language changed',
            'menu_title': 'Main menu'
        }
        mock_get_main_menu.return_value = 'main_menu'
        
        await change_language_en(callback_query, state)
        
        # Verify language was updated
        mock_update_language.assert_called_once_with(
            callback_query.from_user.id,
            "en",
            state
        )
        
        # Verify messages were sent
        assert callback_query.message.answer.call_count == 2
        callback_query.message.answer.assert_any_call(text='Language changed')
        callback_query.message.answer.assert_any_call(
            text='Main menu',
            reply_markup='main_menu'
        )

@pytest.mark.asyncio
async def test_change_notifications(callback_query, state):
    with patch('handlers.settings.get_text', new_callable=AsyncMock) as mock_get_text, \
         patch('handlers.settings.get_notifications_menu', new_callable=AsyncMock) as mock_get_notifications_menu:
        
        mock_get_text.return_value = 'Notifications settings'
        mock_get_notifications_menu.return_value = 'notifications_menu'
        
        await change_notifications(callback_query, state)
        
        callback_query.answer.assert_called_once()
        callback_query.message.delete.assert_called_once()
        callback_query.message.answer.assert_called_once_with(
            text='Notifications settings',
            reply_markup='notifications_menu'
        )

@pytest.mark.asyncio
async def test_menu_sms_notification(callback_query, state):
    with patch('handlers.settings.get_text', new_callable=AsyncMock) as mock_get_text, \
         patch('handlers.settings.get_menu_sms_notification', new_callable=AsyncMock) as mock_get_menu_sms:
        
        mock_get_text.return_value = 'SMS notification settings'
        mock_get_menu_sms.return_value = 'sms_menu'
        
        await menu_sms_notification(callback_query, state)
        
        callback_query.answer.assert_called_once()
        callback_query.message.delete.assert_called_once()
        callback_query.message.answer.assert_called_once_with(
            text='SMS notification settings',
            reply_markup='sms_menu'
        )

@pytest.mark.asyncio
async def test_enable_sms_notification(callback_query, state):
    with patch('handlers.settings.get_texts', new_callable=AsyncMock) as mock_get_texts, \
         patch('handlers.settings.get_main_menu', new_callable=AsyncMock) as mock_get_main_menu:
        
        mock_get_texts.return_value = {
            'sms_enabled': 'SMS notifications enabled',
            'menu_title': 'Main menu'
        }
        mock_get_main_menu.return_value = 'main_menu'
        
        await enable_sms_notification(callback_query, state)
        
        callback_query.answer.assert_called_once()
        callback_query.message.delete.assert_called_once()
        assert callback_query.message.answer.call_count == 2
        callback_query.message.answer.assert_any_call(text='SMS notifications enabled')
        callback_query.message.answer.assert_any_call(
            text='Main menu',
            reply_markup='main_menu'
        )

@pytest.mark.asyncio
async def test_disable_sms_notification(callback_query, state):
    with patch('handlers.settings.get_texts', new_callable=AsyncMock) as mock_get_texts, \
         patch('handlers.settings.get_main_menu', new_callable=AsyncMock) as mock_get_main_menu:
        
        mock_get_texts.return_value = {
            'sms_disabled': 'SMS notifications disabled',
            'menu_title': 'Main menu'
        }
        mock_get_main_menu.return_value = 'main_menu'
        
        await disable_sms_notification(callback_query, state)
        
        callback_query.answer.assert_called_once()
        callback_query.message.delete.assert_called_once()
        assert callback_query.message.answer.call_count == 2
        callback_query.message.answer.assert_any_call(text='SMS notifications disabled')
        callback_query.message.answer.assert_any_call(
            text='Main menu',
            reply_markup='main_menu'
        ) 