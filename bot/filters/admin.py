import logging
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

logger = logging.getLogger(__name__)

# Список глобальных администраторов бота (твои ID), 
# которые могут управлять хелперами и поддержкой в ЛЮБЫХ чатах, даже если бот не админ
GLOBAL_ADMINS = [5165467900]

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Если отправитель — главный админ/создатель, пропускаем сразу без лишних запросов к API
        if message.from_user.id in GLOBAL_ADMINS:
            return True

        if message.chat.type not in ("group", "supergroup"):
            return False

        try:
            # Пытаемся проверить права через Telegram API (сработает, если бот админ)
            member = await message.chat.get_member(message.from_user.id)
            return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        except Exception as e:
            # Если бот не админ, Telegram вернет CHAT_ADMIN_REQUIRED — логируем и мягко возвращаем False
            logger.warning( f"Не удалось проверить права локального админа в чате {message.chat.id} (возможно, бот не админ): {e}" )
            return False
