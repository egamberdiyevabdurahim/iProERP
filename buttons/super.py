from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def main_kb_su():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="User boshqaruvi", callback_data="user_mng"),
            ],
            [
                InlineKeyboardButton(text="Gadget boshqaruvi", callback_data="gadget_mng"),
            ],
            [
                InlineKeyboardButton(text='🔙 Back', callback_data='home')
            ],
        ]
    )
    return keyboard


async def user_mng_kb_su():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Yangi", callback_data="new_user")
            ],
            [
                InlineKeyboardButton(text="O'chirish", callback_data="delete_user"),
            ],
            [
                InlineKeyboardButton(text='🔙 Back', callback_data='super_kb')
            ],
        ]
    )
    return keyboard


async def gadget_mng_kb_su():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hammasini ko'rish 📋", callback_data="show_gadgets")
            ],
            [
                InlineKeyboardButton(text='🔙 Back', callback_data='super_kb')
            ],
        ]
    )
    return keyboard