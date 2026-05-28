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
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS helpers (
                id SERIAL PRIMARY KEY,
                user_id BIGINT UNIQUE,
                tg_nick TEXT,
                roblox_nick TEXT
            )
        ''')
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id SERIAL PRIMARY KEY,
                helper_id INTEGER,
                user_id BIGINT,
                stars INTEGER,
                comment TEXT,
                UNIQUE(helper_id, user_id)
            )
        ''')
        
        # Автоматически добавляем колонку для юзернейма, если её еще нет
        try:
            await conn.execute('ALTER TABLE reviews ADD COLUMN reviewer_username TEXT')
            logger.info("Добавлена колонка reviewer_username.")
        except asyncpg.exceptions.DuplicateColumnError:
            pass # Колонка уже существует, всё ок
            
        logger.info("PostgreSQL database initialized successfully.")
    finally:
        await conn.close()

async def add_helper(user_id: int, tg_nick: str, roblox_nick: str) -> bool:
    conn = await get_connection()
    try:
        await conn.execute(
            "INSERT INTO helpers (user_id, tg_nick, roblox_nick) VALUES ($1, $2, $3)",
            user_id, tg_nick, roblox_nick
        )
        return True
    except asyncpg.UniqueViolationError:
        return False
    finally:
        await conn.close()

async def delete_helper(user_id: int) -> bool:
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT id FROM helpers WHERE user_id = $1", user_id)
        if not row:
            return False
        await conn.execute("DELETE FROM helpers WHERE user_id = $1", user_id)
        return True
    finally:
        await conn.close()

# Обновлено: теперь принимает reviewer_username
async def save_review(helper_id: int, user_id: int, stars: int, comment: str | None = None, reviewer_username: str | None = None):
    conn = await get_connection()
    try:
        await conn.execute('''
            INSERT INTO reviews (helper_id, user_id, stars, comment, reviewer_username) 
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (helper_id, user_id) 
            DO UPDATE SET stars = EXCLUDED.stars, comment = EXCLUDED.comment, reviewer_username = EXCLUDED.reviewer_username
        ''', helper_id, user_id, stars, comment, reviewer_username)
    finally:
        await conn.close()

async def get_helpers_top():
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT h.id, h.tg_nick, h.roblox_nick, 
                   CAST(COALESCE(AVG(r.stars), 0) AS FLOAT) as avg_rating,
                   COUNT(r.id) as review_count
            FROM helpers h
            LEFT JOIN reviews r ON h.id = r.helper_id
            GROUP BY h.id, h.tg_nick, h.roblox_nick
            ORDER BY avg_rating DESC, review_count DESC
        ''')
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
            LEFT JOIN reviews r ON h.id = r.helper_id
            WHERE h.id = $1
            GROUP BY h.id, h.user_id, h.tg_nick, h.roblox_nick
        ''', helper_id)
        return tuple(row) if row else None
    finally:
        await conn.close()

# Обновлено: теперь возвращает ID отзыва и ник
async def get_latest_reviews(helper_id: int, limit: int = 3):
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT id, stars, comment, reviewer_username FROM reviews 
            WHERE helper_id = $1 
            ORDER BY id DESC LIMIT $2
        ''', helper_id, limit)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()

# НОВОЕ: Получить все отзывы
async def get_all_reviews(helper_id: int):
    conn = await get_connection()
    try:
        rows = await conn.fetch('''
            SELECT id, stars, comment, reviewer_username FROM reviews 
            WHERE helper_id = $1 
            ORDER BY id DESC
        ''', helper_id)
        return [tuple(row) for row in rows]
    finally:
        await conn.close()

# НОВОЕ: Проверить, есть ли уже отзыв от этого юзера
async def get_user_review(helper_id: int, user_id: int):
    conn = await get_connection()
    try:
        row = await conn.fetchrow('''
            SELECT stars, comment FROM reviews WHERE helper_id = $1 AND user_id = $2
        ''', helper_id, user_id)
        return tuple(row) if row else None
    finally:
        await conn.close()

# НОВОЕ: Удаление отзыва админом
async def delete_review(review_id: int) -> bool:
    conn = await get_connection()
    try:
        result = await conn.execute("DELETE FROM reviews WHERE id = $1", review_id)
        return result != "DELETE 0"
    finally:
        await conn.close()
