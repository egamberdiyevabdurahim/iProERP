from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from filters.role import RoleFilter
from loader import Gadget
from states.admin import ChangePriceSt
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('change-price_'), RoleFilter([2, 3]))
async def change_price_cl(
        call: types.CallbackQuery,
        state: FSMContext
):
    await vld(o=call, u=call.from_user, delete=True)
    idn = call.data.split("_")[1]
    await state.update_data(idn=idn)
    await call.message.answer(text="Yangi Narxini kiriting:")
    await state.set_state(ChangePriceSt.price)


@router.message(ChangePriceSt.price)
async def price_m(
        message: types.Message,
        state: FSMContext
):
    await vld(o=message, u=message.from_user, delete=True)
    st_data = await state.get_data()
    idn = st_data.get('idn')
    price = message.text.strip()
    if not price.isnumeric():
        await message.answer(text="Narx xato!")
        await state.clear()
        return

    await Gadget.column_updater(
        idn=idn,
        col_name='price',
        data=int(price)
    )
    await state.clear()

    await message.answer(text=f"Narx o'zgartirildi yangi narx: {price}")
