import logging
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

logger = logging.getLogger(__name__)

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type not in ("group", "supergroup"):
            return False

        try:
            member = await message.chat.get_member(message.from_user.id)
            return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        except Exception as e:
            # Теперь мы точно увидим, на что ругается Telegram
            logger.error(f"Ошибка проверки прав в чате {message.chat.id}: {e}")
            return False
