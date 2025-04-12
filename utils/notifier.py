from asyncio import sleep

from aiogram import Bot

from database_config.config import DEVELOPER_ID, GROUP_ID, MOVIE_DATA_GROUP_ID, TOKEN
from utils.additions import tas_t

bot = Bot(token=TOKEN)


async def notice_developer(message, count: int = 1):
    try:
        await bot.send_message(
            text=f"#error {tas_t().strftime('%Y-%m-%d %H:%M-%S')}:\n{message}",
            chat_id=DEVELOPER_ID,
        )
    except Exception:
        if count < 16:
            await sleep(2**count)  # Exponential backoff
            await notice_developer(message, count + 1)


async def notice_admin(message, chat_id, count: int = 1):
    try:
        await bot.send_message(
            text=f"#warning:\n{message}",
            chat_id=chat_id,
        )
    except Exception as e:
        if count < 16:
            await sleep(2**count)  # Exponential backoff
            await notice_admin(message, count + 1)

        else:
            await notice_developer(message=e)


async def notice_group(message, count: int = 1):
    try:
        await bot.send_message(
            text=message,
            chat_id=GROUP_ID,
            parse_mode="HTML"
        )
    except Exception as e:
        if count < 6:
            await sleep(2**count)  # Exponential backoff
            await notice_group(message, count + 1)

        else:
            await notice_developer(message=e)


async def notice_movie_data_group(message, count: int = 1):
    try:
        await bot.send_message(
            text=message,
            chat_id=MOVIE_DATA_GROUP_ID,
            parse_mode="HTML"
        )
    except Exception as e:
        if count < 6:
            await sleep(2**count)  # Exponential backoff
            await notice_movie_data_group(message, count + 1)

        else:
            await notice_developer(message=e)
