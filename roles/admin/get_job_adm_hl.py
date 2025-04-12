from aiogram import types, Router, F

from filters.role import RoleFilter
from loader import Gadget
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('get-job_'), RoleFilter([1,2,3]))
async def get_job_cl(
        call: types.CallbackQuery
):
    u = await vld(o=call, u=call.from_user, delete=True)
    idn = call.data.split("_")[1]

    await Gadget.column_updater(
        idn=idn,
        col_name='status',
        data=1
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='worker',
        data=u.idn
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='start_time',
        data=tas_t()
    )

    await call.message.answer(text='Ish olindi ✅')
