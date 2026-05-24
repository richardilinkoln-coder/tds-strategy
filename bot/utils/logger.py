import logging


def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("aiogram.event").setLevel(logging.INFO)
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
