from aiogram.types import Message, CallbackQuery

from loader import Errors, User, History


async def error_logger(u_idn = None, description=None, error_pl = None):
    user = await User.get_data(u_idn)
    await Errors.create(
        user_id=user.idn,
        description=description,
        error_pl=error_pl
    )
    return None


async def logger(obj: Message | CallbackQuery, user=None):
    chat_id = user.id
    try:
        user = await User.get_data(chat_id)
        await History.create(
            user_id=user.idn,
            message=obj.text if isinstance(obj, Message) else obj.data,
            message_id=obj.message_id if isinstance(obj, Message) else obj.message.message_id
        )
        await user.use()
        return True

    except Exception as e:
        await error_logger(u_idn=chat_id, description=e, error_pl="activity_maker")
        return None