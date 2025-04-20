from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from filters.role import RoleFilter
from loader import Gadget
from roles.admin.my_jobs_adm_hl import my_jobs_cl
from states.admin import SearchBySt
from utils.additions import tas_t
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('search_by_'), RoleFilter([1,2,3]))
async def search_by_cl(
        call: types.CallbackQuery,
        state: FSMContext
):
    await vld(o=call, u=call.from_user, delete=True)
    type_data = call.data.split("_")[-1]
    await state.update_data(type_data=type_data)
    await call.message.answer(
        text="Qidirish uchun kiriting:"
    )
    await state.set_state(SearchBySt.text)


@router.message(SearchBySt.text)
async def search_by_m(
        mess: types.Message,
        state: FSMContext
):
    u = await vld(o=mess, u=mess.from_user)
    text = mess.text
    st_data = await state.get_data()
    type_data = st_data.get('type_data')
    if type_data == 'name':
        data = await Gadget.get_by_search_name(search_query=text)

    elif type_data == 'idn':
        data = await Gadget.get_by_search_idn(search_query=text)

    elif type_data == 'imei':
        data = await Gadget.get_by_search_imei1(search_query=text)

    elif type_data == 'idn':
        data = await Gadget.get_by_search_idn(search_query=text)

    elif type_data == 'idn':
        data = await Gadget.get_by_search_idn(search_query=text)
