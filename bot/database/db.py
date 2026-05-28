import os
import asyncpg
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


async def get_connection():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL variable is missing in environment!")
    return await asyncpg.connect(DATABASE_URL)


async def init_db():
    conn = await get_connection()
    try:
        # Хелперы локальны для каждого чата
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS helpers (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                user_id BIGINT,
                tg_nick TEXT,
                roblox_nick TEXT,
                UNIQUE(chat_id, user_id)
            )
        ''')
        # Отзывы привязаны к глобальному user_id хелпера (общие на все чаты)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                helper_user_id BIGINT,
                user_id BIGINT,
                stars INTEGER,
                comment TEXT,
                reviewer_username TEXT,
                UNIQUE(helper_user_id, user_id)
            )
        ''')
        # Агенты поддержки локальны для каждого чата
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS support_agents (
                id SERIAL PRIMARY KEY,
                chat_id BIGINT,
                tg_nick TEXT,
                UNIQUE(chat_id, tg_nick)
            )
        ''')
        logger.info("PostgreSQL database initialized successfully.")
    finally:
        await conn.close()


async def add_helper(chat_id: int, user_id: int, tg_nick: str, roblox_nick: str) -> bool:
    conn = await get_connection()
    try:
        await conn.execute(
            "INSERT INTO helpers (chat_id, user_id, tg_nick, roblox_nick) VALUES ($1, $2, $3, $4) "
            "ON CONFLICT (chat_id, user_id) DO NOTHING",
            chat_id, user_id, tg_nick, roblox_nick
        )
        return True
    except asyncpg.UniqueViolationError:
        return False
    finally:
        await conn.close()


async def delete_helper(chat_id: int, user_id: int) -> bool:
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT id FROM helpers WHERE chat_id = $1 AND user_id = $2", chat_id, user_id)
        if not row:
            return False
        await conn.execute("DELETE FROM helpers WHERE chat_id = $1 AND user_id = $2", chat_id, user_id)
        return True
    finally:
        await conn.close()


async def save_review(helper_user_id: int, user_id: int, stars: int, comment: str | None = None, reviewer_username: str | None = None):
    conn = await get_connection()
    try:
        await conn.execute('''
            INSERT INTO reviews (helper_user_id, user_id, stars, comment, reviewer_username) 
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (helper_user_id, user_id) 
            DO UPDATE SET stars = EXCLUDED.stars, comment = EXCLUDED.comment, reviewer_username = EXCLUDED.reviewer_username
        ''', helper_user_id, user_id, stars, comment, reviewer_username)
    finally:
        await conn.close()


async def get_helpers_top(chat_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT h.id, h.tg_nick, h.roblox_nick, 
                   CAST(COALESCE(AVG(r.stars), 0) AS FLOAT) as avg_rating,
                   COUNT(r.id) as review_count
            FROM helpers h
            LEFT JOIN reviews r ON h.user_id = r.helper_user_id
            WHERE h.chat_id = $1
            GROUP BY h.id, h.tg_nick, h.roblox_nick
            ORDER BY avg_rating DESC, review_count DESC
        ''', chat_id)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()


async def get_helper_info(helper_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow('''
            SELECT h.user_id, h.tg_nick, h.roblox_nick, 
                   CAST(COALESCE(AVG(r.stars), 0) AS FLOAT) as avg_rating,
                   COUNT(r.id) as review_count
            FROM helpers h
            LEFT JOIN reviews r ON h.user_id = r.helper_user_id
            WHERE h.id = $1
            GROUP BY h.id, h.user_id, h.tg_nick, h.roblox_nick
        ''', helper_id)
        return tuple(row) if row else None
    finally:
        await conn.close()


async def get_latest_reviews(helper_user_id: int, limit: int = 3):
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT id, stars, comment, reviewer_username FROM reviews 
            WHERE helper_user_id = $1 
            ORDER BY id DESC LIMIT $2
        ''', helper_user_id, limit)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()


async def get_all_reviews(helper_user_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT id, stars, comment, reviewer_username FROM reviews 
            WHERE helper_user_id = $1 
            ORDER BY id DESC
        ''', helper_user_id)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()


async def get_user_review(helper_user_id: int, user_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow('''
            SELECT stars, comment FROM reviews WHERE helper_user_id = $1 AND user_id = $2
        ''', helper_user_id, user_id)
        return tuple(row) if row else None
    finally:
        await conn.close()


async def delete_review(review_id: int) -> bool:
    conn = await get_connection()
    try:
        result = await conn.execute("DELETE FROM reviews WHERE id = $1", review_id)
        return result != "DELETE 0"
    finally:
        await conn.close()


# Методы для управления агентами поддержки чата
async def add_support_agent(chat_id: int, tg_nick: str) -> bool:
    conn = await get_connection()
    try:
        await conn.execute(
            "INSERT INTO support_agents (chat_id, tg_nick) VALUES ($1, $2) "
            "ON CONFLICT (chat_id, tg_nick) DO NOTHING",
            chat_id, tg_nick.replace("@", "")
        )
        return True
    except Exception:
        return False
    finally:
        await conn.close()


async def delete_support_agent(chat_id: int, tg_nick: str) -> bool:
    conn = await get_connection()
    try:
        result = await conn.execute(
            "DELETE FROM support_agents WHERE chat_id = $1 AND tg_nick = $2",
            chat_id, tg_nick.replace("@", "")
        )
        return result != "DELETE 0"
    finally:
        await conn.close()


async def get_support_agents(chat_id: int) -> list[str]:
    conn = await get_connection()
    try:
        rows = await conn.fetch("SELECT tg_nick FROM support_agents WHERE chat_id = $1", chat_id)
        return [row["tg_nick"] for row in rows]
    finally:
        await conn.close()
