import aiosqlite
import logging

logger = logging.getLogger(__name__)
DB_PATH = "helpers.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Таблица хелперов
        await db.execute('''
            CREATE TABLE IF NOT EXISTS helpers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                tg_nick TEXT,
                roblox_nick TEXT
            )
        ''')
        # Таблица отзывов (UNIQUE защищает от накрутки: 1 юзер = 1 отзыв на хелпера)
        await db.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                helper_id INTEGER,
                user_id INTEGER,
                stars INTEGER,
                comment TEXT,
                UNIQUE(helper_id, user_id)
            )
        ''')
        await db.commit()
        logger.info("Database initialized.")

async def add_helper(user_id: int, tg_nick: str, roblox_nick: str) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        try:
            await db.execute(
                "INSERT INTO helpers (user_id, tg_nick, roblox_nick) VALUES (?, ?, ?)",
                (user_id, tg_nick, roblox_nick)
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False # Хелпер с таким user_id уже есть

async def get_helpers_top():
    """Возвращает список хелперов, отсортированный по среднему рейтингу и количеству отзывов."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT h.id, h.tg_nick, h.roblox_nick, 
                   IFNULL(AVG(r.stars), 0) as avg_rating,
                   COUNT(r.id) as review_count
            FROM helpers h
            LEFT JOIN reviews r ON h.id = r.helper_id
            GROUP BY h.id
            ORDER BY avg_rating DESC, review_count DESC
        ''') as cursor:
            return await cursor.fetchall()

async def get_helper_info(helper_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT h.user_id, h.tg_nick, h.roblox_nick, 
                   IFNULL(AVG(r.stars), 0) as avg_rating,
                   COUNT(r.id) as review_count
            FROM helpers h
            LEFT JOIN reviews r ON h.id = r.helper_id
            WHERE h.id = ?
            GROUP BY h.id
        ''', (helper_id,)) as cursor:
            return await cursor.fetchone()

async def get_latest_reviews(helper_id: int, limit: int = 3):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('''
            SELECT stars, comment FROM reviews 
            WHERE helper_id = ? 
            ORDER BY id DESC LIMIT ?
        ''', (helper_id, limit)) as cursor:
            return await cursor.fetchall()



# Добавить в конец файла bot/database/db.py
async def save_review(helper_id: int, user_id: int, stars: int, comment: str | None = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO reviews (helper_id, user_id, stars, comment) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(helper_id, user_id) DO UPDATE SET 
            stars=excluded.stars, comment=excluded.comment
        ''', (helper_id, user_id, stars, comment))
        await db.commit()


# Измененная функция в bot/database/db.py

async def delete_helper(user_id: int) -> bool:
    """Удаляет только хелпера по его Telegram ID. Отзывы остаются в базе."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Проверяем, есть ли такой хелпер вообще
        async with db.execute("SELECT id FROM helpers WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if not row:
                return False  # Хелпер не найден
        
        # Удаляем хелпера из списка, но таблицу reviews НЕ трогаем
        await db.execute("DELETE FROM helpers WHERE user_id = ?", (user_id,))
        await db.commit()
        return True
