from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from buttons.main import skip_kb_kb
from filters.role import RoleFilter
from loader import Gadget
from states.admin import WorksSt
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('works_'), RoleFilter([1,2]))
async def works_cl(
        call: types.CallbackQuery,
        state: FSMContext
):
    await vld(o=call, u=call.from_user, delete=True)
    idn = call.data.split("_")[1]
    await state.update_data(idn=idn)
    await call.message.answer(text="Xarajatni kiriting:", reply_markup=await skip_kb_kb())
    await state.set_state(WorksSt.expense)


@router.message(WorksSt.expense)
async def expense_m(
        message: types.Message,
        state: FSMContext
):
    await vld(o=message, u=message.from_user, delete=True)
    st_data = await state.get_data()
    idn = st_data.get('idn')
    expense = message.text.strip()
    if not expense.isnumeric():
        await message.answer(text="Xarajat xato!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    if expense == "O'tkazib yuborish":
        expense = None

    await Gadget.column_updater(
        idn=idn,
        col_name='expense',
        data=expense
    )

    await Gadget.column_updater(
        idn=idn,
        col_name='status',
        data=2
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='stop_time',
        data=tas_t()
    )
    data = await Gadget.get_data(idn=idn)
    duration = (data.end_time - data.start_time) - data.stop_duration
    await state.clear()

    await message.answer(text=f'Remont vaqti: {duration}', reply_markup=ReplyKeyboardRemove())
