import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Импорты твоих старых модулей
from bot.handlers.strategy import router

# Импорты новых модулей хелперов и базы данных
from bot.database import db
from bot.handlers.helpers import router as helpers_router


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


async def main() -> None:
    load_dotenv()
    setup_logging()

    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN not found in .env")

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    bot = Bot(
        token=token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    dp = Dispatcher(storage=MemoryStorage())

    # 1. ПОДКЛЮЧАЕМ РОУТЕРЫ
    # Сначала твой старый роутер стратегий
    dp.include_router(router)
    # Сразу под ним подключаем новый роутер хелперов
    dp.include_router(helpers_router)

    # Удаляем старые накопленные апдейты
    await bot.delete_webhook(drop_pending_updates=True)

    # 2. ИНИЦИАЛИЗИРУЕМ БАЗУ ДАННЫХ
    # Создаем файл базы данных и таблицы прямо перед запуском бота
    await db.init_db()

    logging.info("Starting TDS strategy bot...")

    try:
        await dp.start_polling(
            bot,
            allowed_updates=dp.resolve_used_update_types(),
        )

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
