from asyncpg import Pool

async def get_user_by_id(user_id: int, db: Pool) -> dict | None:
    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users_telegram WHERE user_id = $1", user_id)
        return row if row else None

async def get_user_language(user_id: int, db: Pool) -> str | None:
    async with db.acquire() as conn:
        row = await conn.fetchrow("SELECT language FROM users_telegram WHERE user_id = $1", user_id)
        return row["language"] if row else None

async def save_user_language(user_id: int, lang: str, db: Pool) -> None:
    async with db.acquire() as conn:
        await conn.execute(
            "INSERT INTO users_telegram (user_id, language) VALUES ($1, $2) "
            "ON CONFLICT (user_id) DO UPDATE SET language = $2",
            user_id, lang
        )

async def upsert_user(user_id: int, username: str | None, first_name: str | None, last_name: str | None, lang: str, db: Pool):
    async with db.acquire() as conn:
        await conn.execute("""
            INSERT INTO users_telegram (user_id, username, first_name, last_name, language)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (user_id) DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                language = EXCLUDED.language,
                updated_at = now()
        """, user_id, username, first_name, last_name, lang)