from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from buttons.main import skip_kb_kb
from filters.role import RoleFilter
from loader import Gadget
from states.admin import NotWorksSt
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('not-works_'), RoleFilter([1,2]))
async def not_works_cl(
        call: types.CallbackQuery,
        state: FSMContext
):
    await vld(o=call, u=call.from_user, delete=True)
    idn = call.data.split("_")[1]
    await state.update_data(idn=idn)
    await call.message.answer(text="Xarajatni kiriting:", reply_markup=await skip_kb_kb())
    await state.set_state(NotWorksSt.expense)


@router.message(NotWorksSt.expense)
async def not_works_expense(
        message: types.Message,
        state: FSMContext
):
    await vld(o=message, u=message.from_user)
    st_data = await state.get_data()
    idn = st_data.get('idn')
    expense = message.text.strip()
    if expense == "O'tkazib yuborish":
        expense = None

    elif not expense.isnumeric():
        await message.answer(text="Xarajat xato!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return

    if expense:
        await Gadget.column_updater(
            idn=idn,
            col_name='expense',
            data=expense
        )

    await Gadget.column_updater(
        idn=idn,
        col_name='status',
        data=3
    )
    await Gadget.column_updater(
        idn=idn,
        col_name='end_time',
        data=tas_t()
    )
    await state.clear()

    await message.answer(text='Ish ishlamadi deb belgilandi ✅', reply_markup=ReplyKeyboardRemove())
