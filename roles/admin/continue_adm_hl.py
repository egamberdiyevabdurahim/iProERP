from aiogram import types, Router, F

from filters.role import RoleFilter
from loader import Gadget
from roles.admin.my_jobs_adm_hl import my_jobs_cl
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('continue_'), RoleFilter([1,2]))
async def continue_cl(
        call: types.CallbackQuery,
        redirect=True,
        idn=None
):
    await vld(o=call, u=call.from_user, delete=True)
    if not idn:
        idn = call.data.split("_")[1]

    data = await Gadget.get_data(idn=idn)
    if data.is_stopped is False:
        await call.message.answer(text="Bu allaqachon davom ettirilgan!")

    else:
        duration = int((tas_t() - data.stop_start_time).total_seconds() // 60)+data.stop_duration
        print(duration)
        print(data.stop_duration)
        await Gadget.column_updater(
            idn=idn,
            col_name='stop_duration',
            data=duration
        )
        await Gadget.column_updater(
            idn=idn,
            col_name='stop_start_time',
            data=None
        )
        await Gadget.column_updater(
            idn=idn,
            col_name='is_stopped',
            data=False
        )
        if redirect:
            await call.message.answer(text="Ish davom ettirildi ✅")

    if redirect:
        await my_jobs_cl(call, delete=False)
