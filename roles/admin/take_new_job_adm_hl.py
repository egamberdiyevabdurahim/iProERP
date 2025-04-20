from aiogram import types, Router, F

from buttons.admin import get_job_adm_kb
from filters.role import RoleFilter
from loader import Gadget, Model
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('get_work_'), RoleFilter([1,2]))
async def get_work_cl(
        call: types.CallbackQuery,
        page=1,
        page_size=1
):
    u = await vld(o=call, u=call.from_user)

    start_index = (page - 1) * page_size
    current_gadgets = await Gadget.get_all(
        ex="AND status = 0",
        st=start_index,
        lt=page_size
    ) or []
    total_gadgets = await Gadget.get_all_count(
        ex=f"AND status = 0",
        st=start_index,
        lt=page_size
    )
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n"

    end_index = start_index + page_size

    counter = end_index
    for gadget in current_gadgets:
        model = await Model.get_data(gadget.model)
        text_data += (
            f"<b>{counter}).</b>\n"
            f"<b>ID</b>: {gadget.idn}\n"
            f"<b>Model</b>: {model.name}\n"
            f"<b>Nomi</b>: {gadget.name}\n"
            f"<b>IMEI&Serial</b>: {gadget.imei1} | {gadget.imei2} | {gadget.serial_number}\n"
            f"<b>Mijoz</b>: {gadget.client_name}\n"
            f"<b>Telefon raqam</b>: {gadget.client_phone_number}\n"
            f"<b>Narxi</b>: {gadget.price}\n"
            f"<b>Yana</b>: {gadget.description[:33]}...")
        counter -= 1

    try:
        await call.message.edit_text(text=text_data,
                                     parse_mode='HTML',
                                     reply_markup=await get_job_adm_kb(
                                         page=page,
                                         page_size=page_size,
                                         u=u,
                                         total_pages=total_pages,
                                         current_gadgets=current_gadgets
                                     ))

    except Exception:
        await call.message.answer(text=text_data,
                                  parse_mode='HTML',
                                  reply_markup=await get_job_adm_kb(
                                      page=page,
                                      page_size=page_size,
                                      u=u,
                                      total_pages=total_pages,
                                      current_gadgets=current_gadgets
                                  ))
