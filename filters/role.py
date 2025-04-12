from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from loader import User
from utils.logger import error_logger


class RoleFilter(BaseFilter):
    def __init__(self, roles: list[int]):
        self.roles = roles

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        chat_id = obj.from_user.id

        try:
            user = await User.get_data(chat_id)

            if user:
                if user.role in self.roles:
                    return True
            return False

        except Exception as e:
            await error_logger(u_idn=chat_id, description=e, error_pl='RoleFilter')
            return False