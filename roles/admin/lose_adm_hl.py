from aiogram import types, Router, F

from filters.role import RoleFilter
from loader import Gadget, GadgetWorkers
from roles.admin.my_jobs_adm_hl import my_jobs_cl
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('lose_'), RoleFilter([1, 2, 3]))
async def lose_cl(
        call: types.CallbackQuery
):
    u = await vld(o=call, u=call.from_user, delete=True)
    idn = call.data.split("_")[1]

    data = await Gadget.get_data(idn=idn)
    await Gadget.column_updater(
        idn=idn,
        col_name='status',
        data=0
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='worker',
        data=None
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='start_time',
        data=None
    )
    await GadgetWorkers.create(
        user_id=data.worker,
        gadget=data.idn
    )

    await call.message.answer(text='Ish kechildi ✅')
    await my_jobs_cl(call)
