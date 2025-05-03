from db.user_repo import get_user_language, save_user_language, upsert_user
from utils.i18n import resolve_language
from asyncpg import Pool

async def get_or_create_user(message, db: Pool) -> str:
    user_id = message.from_user.id
    lang = await get_user_language(user_id, db)
    resolved = resolve_language(message.from_user.language_code)

    await upsert_user(
        user_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        lang=resolved,
        db=db
    )

    return lang or resolved

async def update_user_language(user_id: int, lang: str, db: Pool) -> None:
    await save_user_language(user_id, lang, db)