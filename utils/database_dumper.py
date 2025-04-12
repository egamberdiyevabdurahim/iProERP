import os
import subprocess

from aiogram.types import FSInputFile

from database_config.config import GROUP_ID, DB_USER, DB_NAME, DB_HOST, DB_PORT, DB_PASS
from loader import bot
from utils.notifier import notice_developer
from utils.additions import BASE_PATH, tas_t

DUMP_PATH = f"{BASE_PATH}/database.sql"


async def send_dump_to_telegram():
    """Send the database dump to a Telegram group."""
    if os.path.exists(DUMP_PATH):
        document = FSInputFile(DUMP_PATH)
        try:
            await bot.send_document(
                chat_id=GROUP_ID,
                document=document,
                caption=tas_t().strftime("%Y-%m-%d %H:%M"),
            )
        except Exception as e:
            await notice_developer(message=f"Failed to dump database: {str(e)}")

        finally:
            os.remove(DUMP_PATH)
    else:
        await notice_developer(message=f"Dump file does not exist")

async def dump_and_send():
    """Dump the database and send the file to Telegram."""
    try:
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)

        dump_command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} -F p -d {DB_NAME} -f {DUMP_PATH}"
        env = os.environ.copy()
        env["PGPASSWORD"] = DB_PASS

        subprocess.run(dump_command, shell=True, check=True, env=env)

        await send_dump_to_telegram()
    except subprocess.CalledProcessError as e:
        await notice_developer(message=f"Failed to dump database: {str(e)}"
                                       f"Command output: {str(e.output)}")

    except Exception as general_error:
        await notice_developer(message=f"An unexpected error occurred: {str(general_error)}")
