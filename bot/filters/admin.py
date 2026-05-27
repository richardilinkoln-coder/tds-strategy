# bot/filters/admin.py
import os
from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Просто впиши сюда ID админов напрямую вместо чтения из .env
        admins = [5165467900]  # <-- Замени эти цифры на реальные TG ID
        
        return message.from_user.id in admins
