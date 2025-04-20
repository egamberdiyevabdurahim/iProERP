import asyncio
import schedule

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from roles.admin import (
    continue_adm_hl, detailed_adm_hl, get_job_adm_hl, lose_adm_hl, main_adm_hl,
    my_jobs_adm_hl, not_works_adm_hl, register_adm_hl, stop_adm_hl,
    take_new_job_adm_hl, works_adm_hl, change_price_adm_hl, find_gadget, change_price_hl
)
from roles.super import (
    main_super_hl, user_mg_adm_hl, gadget_mg_adm_hl
)
from main import router

from loader import bot, dp


@dp.message(Command('support', 'help'))
async def support_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Yordam Uchun: @iProServis✅")


async def schedule_task_for_inactivate():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    dp.include_routers(
        router,

        # SUPER
        main_super_hl.router,
        user_mg_adm_hl.router,
        gadget_mg_adm_hl.router,

        continue_adm_hl.router,
        detailed_adm_hl.router,
        get_job_adm_hl.router,
        lose_adm_hl.router,
        main_adm_hl.router,
        my_jobs_adm_hl.router,
        not_works_adm_hl.router,
        register_adm_hl.router,
        stop_adm_hl.router,
        take_new_job_adm_hl.router,
        works_adm_hl.router,
        change_price_adm_hl.router,
        find_gadget.router,
        change_price_hl.router,
    )
    # dp.update.outer_middleware(middleware=ErrorLoggingMiddleware())
    # dp.update.middleware(middleware=SubscriptionMiddleware())
    await dp.start_polling(bot)

async def init():
    # schedule.every().day.at("19:00").do(lambda: asyncio.create_task(dump_and_send()))
    await asyncio.gather(main(), schedule_task_for_inactivate())

if __name__ == '__main__':
    try:
        asyncio.run(init())
    except Exception as e:
        print(e)
