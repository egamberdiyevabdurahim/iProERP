from aiogram import types, Router, F

from buttons.admin import get_job_adm_kb
from filters.role import RoleFilter
from loader import Gadget, Model, User
from utils.validator import vld

router = Router()


def get_status_text(status: int) -> str:
    return {
        0: 'Kutilmoqda 🔹',
        1: 'Jarayonda ♻️',
        2: 'Tuzatildi ✅',
        3: 'Oxshamadi ❌'
    }.get(status, 'Nomaʼlum')


async def get_worker_name(worker_idn: int) -> str:
    if not worker_idn:
        return ''
    user = await User.get_by_idn(idn=worker_idn)
    return f"{user.first_name} {user.last_name or ''}"


@router.callback_query(F.data.startswith('change_price_'), RoleFilter([1, 2, 3]))
async def change_price_gadgets_cl(
        call: types.CallbackQuery,
        page=1,
        page_size=1
):
    u = await vld(o=call, u=call.from_user)

    start_index = (page - 1) * page_size

    current_gadgets = await Gadget.get_all(
        ex="AND is_deleted is False",
        st=start_index,
        lt=page_size
    ) or []
    total_gadgets = await Gadget.get_all_count()
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n"

    end_index = start_index + page_size

    counter = end_index
    for gadget in current_gadgets:
        status = get_status_text(gadget.status)
        model = await Model.get_data(gadget.model)
        worker = None
        if gadget.status != 1:
            worker = await get_worker_name(gadget.worker)
        text_data += (
            f"<b>{counter}). -- {status}</b>\n"
            f"<b>ID</b>: {gadget.idn}\n"
            f"<b>Model</b>: {model.name}\n"
            f"<b>Nomi</b>: {gadget.name}\n"
            f"<b>IMEI&Serial</b>: {gadget.imei1} | {gadget.imei2} | {gadget.serial_number}\n"
            f"<b>Mijoz</b>: {gadget.client_name}\n"
            f"<b>Telefon raqam</b>: {gadget.client_phone_number}\n"
            f"<b>Narxi</b>: {gadget.price}\n"
            f"<b>Yana</b>: {gadget.description[:33]}...")
        if worker:
            text_data += f"<b>Ishchi</b>: {gadget.worker}\n"
        counter -= 1

    try:
        await call.message.edit_text(text=text_data,
                                     parse_mode='HTML',
                                     reply_markup=await get_job_adm_kb(
                                         page=page,
                                         page_size=page_size,
                                         u=u,
                                         total_pages=total_pages,
                                         current_gadgets=current_gadgets,
                                         change=True,
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
