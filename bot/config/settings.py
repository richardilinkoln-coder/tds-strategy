from dataclasses import dataclass
import os


@dataclass(slots=True)
class Settings:
    bot_token: str


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token:
        raise ValueError("BOT_TOKEN is missing. Create .env and set BOT_TOKEN=...")
    return Settings(bot_token=token)

# Список агентов поддержки
SUPPORT_AGENTS = [
    "qzeyc",
    "richardilinkoln",
    "ктото_еще"
]
