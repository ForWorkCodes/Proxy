from utils.i18n import resolve_language
from aiogram.fsm.context import FSMContext
from services.proxy_api_client import ProxyAPIClient

user_service = ProxyAPIClient()


async def create_user(message, state: FSMContext) -> dict:
    if message.from_user.is_bot:
        print("⚠️ Сообщение от бота, пропускаем")
        return None
    
    user_id = message.from_user.id
    data = await state.get_data()
    if "user" in data:
        print("Пользователь получен из кэша", data["user"])
        return data["user"]

    resolved_lang = resolve_language(message.from_user.language_code)
    user_db = await user_service.get_user(user_id)

    if user_db:
        print("Пользователь найден в базе данных")
        user = {
            "user_id": user_db['telegram_id'],
            "username": user_db['username'],
            "firstname": user_db['firstname'],
            "language": user_db['language'],
            "active": user_db['active'],
            "banned": user_db['banned']
        }
    else:
        print("Пользователь не найден в базе данных")
        user = await user_service.upsert_user(
            telegram_id=user_id,
            chat_id=message.chat.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            language=resolved_lang,
        )
        
        if user is None:
            await message.answer("⚠️ Error creating user. Please try again later.")
            print("❌ Критическая ошибка: не удалось создать пользователя")
            return
    
    print("-----------------------------")
    print(user)
    print("-----------------------------")

    await state.update_data(user=user)
    return user


async def update_user_language(user_id: int, lang: str, state: FSMContext) -> None:
    await user_service.update_language(user_id, lang)
    data = await state.get_data()
    
    if "user" in data:
        user = data["user"]
        user["language"] = lang
        print("language updated: ", lang)
        await state.update_data(user=user)