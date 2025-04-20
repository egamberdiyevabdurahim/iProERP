from aiogram import types, Router, F

from filters.role import RoleFilter
from loader import Gadget
from roles.admin.my_jobs_adm_hl import my_jobs_cl
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('stop_'), RoleFilter([1,2]))
async def stop_cl(
        call: types.CallbackQuery,
        idn = None,
        redirect=True,
        auto_run=False
):
    u = await vld(o=call, u=call.from_user, delete=True)
    if not idn:
        idn = call.data.split("_")[1]

    data = await Gadget.get_data(idn=idn)
    if data.is_stopped:
        await call.message.answer(text="Bu allaqachon to'xtatilgan!")

    else:
        await Gadget.column_updater(
            idn=idn,
            col_name='stop_start_time',
            data=tas_t()
        )
        await Gadget.column_updater(
            idn=idn,
            col_name='is_stopped',
            data=True
        )
        await Gadget.column_updater(
            idn=idn,
            col_name='auto_run',
            data=auto_run
        )
        if not auto_run:
            await call.message.answer(text="Ish to'xtatildi ✅")

    if redirect:
        await my_jobs_cl(call, delete=False)
