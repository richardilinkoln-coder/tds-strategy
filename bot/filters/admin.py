from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type not in ("group", "supergroup"):
            return False

        try:
            member = await message.chat.get_member(message.from_user.id)
            return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
        except Exception:
            return False
