from db.user_repo import get_user_language, save_user_language, upsert_user, get_user_by_id
from utils.i18n import resolve_language
from aiogram.fsm.context import FSMContext

from asyncpg import Pool

async def create_user(message, db: Pool, state: FSMContext) -> dict:
    user_id = message.from_user.id

    data = await state.get_data()
    if "user" in data:
        print("Пользователь получен из кэша")
        return data["user"]

    resolved_lang = resolve_language(message.from_user.language_code)

    user_db = await get_user(user_id, db)

    if user_db:
        print("Пользователь найден в базе данных")
        user = {
            "user_id": user_db['user_id'],
            "username": user_db['username'],
            "first_name": user_db['first_name'],
            "last_name": user_db['last_name'],
            "lang": user_db['language']
        }
    else:
        print("Пользователь не найден в базе данных")
        user = {
            "user_id": user_id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "lang": resolved_lang
        }
        await upsert_user(
            user_id=user_id,
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            lang=resolved_lang,
            db=db
        )

    await state.update_data(user=user)
    return user

async def get_user(user_id: int, db: Pool):
    return await get_user_by_id(user_id, db)

async def update_user_language(user_id: int, lang: str, db: Pool, state: FSMContext) -> None:
    await save_user_language(user_id, lang, db)

    data = await state.get_data()
    user = data.get("user")
    if user:
        user["lang"] = lang
        await state.update_data(user=user)

async def get_language(user_id: int, db: Pool) -> None:
    await get_user_language(user_id, db)