from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


async def skip_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="O'tkazib yuborish", callback_data="skip")
        ]
    ])
    return kb


async def skip_kb_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="O'tkazib yuborish")
        ]
    ], resize_keyboard=True)
    return kb


async def back_kb(back):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🔙 Ortga", callback_data=back)
        ]
    ])
    return kb
