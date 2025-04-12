import aiogram.types
from aiogram.types import Message, CallbackQuery

from loader import User
from utils.logger import logger, error_logger
from utils.message_deleter import message_deleter
from utils.message_sender import send_m


async def vld(
        o: Message | CallbackQuery = None,
        u: aiogram.types.User = None,
        ans: bool = True,
        ans_mg: str = None,
        ans_url: str = None,
        show_alert: bool = None,
        delete: bool = None,
        delete_ex: bool = None,
        delete_ex_ex: bool = None,
        val_type: int = None,
        r_u: bool = True
):
    u_id = u.id
    try:
        o_m = False if isinstance(o, Message) else True
        await logger(obj=o, user=u)

        if ans and o_m:
            await o.answer(text=ans_mg, show_alert=show_alert, url=ans_url)

        if delete:
            if o_m:
                await message_deleter(u_id=u_id, message_id=o.message.message_id)

            else:
                await message_deleter(u_id=u_id, message_id=o.message_id)

        if delete_ex:
            if o_m:
                await message_deleter(u_id=u_id, message_id=o.message.message_id-1)

            else:
                await message_deleter(u_id=u_id, message_id=o.message_id-1)

        if delete_ex_ex:
            if o_m:
                await message_deleter(u_id=u_id, message_id=o.message.message_id - 2)

            else:
                await message_deleter(u_id=u_id, message_id=o.message_id - 2)

        if val_type == 1:
            if o.text.isalpha():
                return None

            else:
                await send_m(u=u, ms="Xatolik: Kiritilgan narsa harf bo'lishi kerak")

        elif val_type == 2:
            if not o.text.isnumeric():
                return None

            else:
                await send_m(u=u, ms="Xatolik: Kiritilgan narsa son bo'lishi kerak")

        elif val_type == 3:
            if not o.text.replace(" ", "").isalnum():
                return None

            else:
                await send_m(u=u, ms="Xatolik: Kiritilgan narsa hammasi harf-numerik bo'lishi kerak")

        if r_u:
            user = await User.get_data(chat_id=u.id)
            return user

    except Exception as e:
        await error_logger(u_idn=u_id, description=e, error_pl="validator")
        return None