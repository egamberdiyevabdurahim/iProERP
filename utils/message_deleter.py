from loader import bot


async def message_deleter(u_id, message_id):
    try:
        await bot.delete_message(chat_id=u_id, message_id=message_id)

    except Exception:
        pass