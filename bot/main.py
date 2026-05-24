import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.strategy import router




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
            parse_mode=ParseMode.MARKDOWN_V2
        ),
    )

    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)

    # Удаляем старые накопленные апдейты
    await bot.delete_webhook(drop_pending_updates=True)

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
