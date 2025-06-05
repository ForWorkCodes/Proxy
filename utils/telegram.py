import logging
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

logger = logging.getLogger(__name__)


async def safe_delete_message(obj):
    try:
        if isinstance(obj, Message):
            await obj.delete()
        elif isinstance(obj, CallbackQuery):
            if obj.message:
                await obj.bot.delete_message(
                    chat_id=obj.message.chat.id,
                    message_id=obj.message.message_id
                )
            else:
                logger.warning("CallbackQuery не содержит message.")
        else:
            logger.warning(f"safe_delete_message: неподдерживаемый тип объекта {type(obj)}")
    except TelegramBadRequest as e:
        chat_id = (
            obj.chat.id if isinstance(obj, Message) else
            obj.message.chat.id if isinstance(obj, CallbackQuery) and obj.message else 'неизвестно'
        )
        message_id = (
            obj.message_id if isinstance(obj, Message) else
            obj.message.message_id if isinstance(obj, CallbackQuery) and obj.message else 'неизвестно'
        )
        logger.warning(f"Не удалось удалить сообщение {message_id} в чате {chat_id}: {e}")
