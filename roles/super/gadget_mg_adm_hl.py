import os
from aiogram import types, Router, F
from aiogram.types import FSInputFile
from filters.role import RoleFilter
from loader import Gadget, Model, User
from utils.additions import BASE_PATH
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


@router.callback_query(F.data == "show_gadgets", RoleFilter([2]))
async def show_gadgets_cl(call: types.CallbackQuery):
    await vld(o=call, u=call.from_user)
    gadgets = await Gadget.get_all()

    if not gadgets:
        await call.message.answer("Hechqanday gadget yo'q!")
        return

    file_path = os.path.join(BASE_PATH, "gadgets.txt")

    with open(file_path, "w", encoding="utf-8") as f:
        for gadget in gadgets:
            model = await Model.get_data(idn=gadget.model)

            imei = f"{gadget.imei1}/{gadget.imei2}" if gadget.imei2 else gadget.imei1
            status = get_status_text(gadget.status)
            worker = None
            if gadget.status != 1:
                worker = await get_worker_name(gadget.worker)

            info = (
                f"{status}\n"
                f"ID: {gadget.idn}\n"
                f"Nomi: {model.name} {gadget.name}\n"
                f"Narxi: {gadget.price}\n"
                f"Xarajat: {gadget.expense}\n"
                f"IMEI: {imei}\n"
                f"S/N: {gadget.serial_number}\n"
                f"Mijoz ismi: {gadget.client_name}\n"
                f"Mijoz telefoni: {gadget.client_phone_number}\n"
            )

            if worker:
                info += f"Ishchi: {worker}\n"

            if gadget.status != 0:
                info += (
                    f"To'xtatilganmi: {'✅' if gadget.is_stopped else '❌'}\n"
                    f"Boshlangan: {gadget.start_time.strftime('%Y-%m-%d %H:%M')}\n"
                )

            if gadget.status in (2, 3):
                info += f"Tugadi: {gadget.end_time.strftime('%Y-%m-%d %H:%M')}\n"

            info += (
                f"Yaratilgan: {gadget.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"Yangilangan: {gadget.updated_at.strftime('%Y-%m-%d %H:%M')}\n"
                f"Qo‘shimcha: {gadget.description}\n"
                f"{'-' * 25}\n"
            )
            f.write(info)

    file = FSInputFile(file_path)
    await call.message.answer_document(file, caption=f"Jami: {len(gadgets)} ta gadget")
    os.remove(file_path)
