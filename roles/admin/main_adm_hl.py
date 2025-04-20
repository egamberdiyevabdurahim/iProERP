from aiogram import types, Router, F

from buttons.admin import started_work_adm_kb, menu_adm_kb, others_adm_kb
from buttons.super import main_kb_su
from filters.role import RoleFilter
from loader import DailyReportWorker, Gadget
from roles.admin.change_price_hl import change_price_gadgets_cl
from roles.admin.continue_adm_hl import continue_cl

from roles.admin.my_jobs_adm_hl import my_jobs_cl
from roles.admin.stop_adm_hl import stop_cl
from roles.admin.take_new_job_adm_hl import get_work_cl
from utils.validator import vld

router = Router()


@router.callback_query(F.data=='start_work', RoleFilter(roles=[1,2,3]))
async def start_work_cl(call: types.CallbackQuery | types.Message, u = None):
    if u is None:
        u = call.from_user
    u = await vld(o=call, u=u)
    await DailyReportWorker.create(user_id=u.idn)
    datas = await Gadget.get_all(
        ex=f'AND worker={u.idn} AND is_stopped is True AND auto_run is True',
    )
    if len(datas) > 0:
        for data in datas:
            await Gadget.column_updater(
                idn=data.idn,
                col_name='auto_run',
                data=False
            )
            await continue_cl(
                call=call,
                redirect=False,
                idn=data.idn
            )
    if isinstance(call, types.Message):
        try:
            await call.edit_text(text='Ish boshlandi!', reply_markup=await started_work_adm_kb(u=u))

        except Exception:
            await call.answer(text='Ish boshlandi!', reply_markup=await started_work_adm_kb(u=u))

    else:
        try:
            await call.message.edit_text(text='Ish boshlandi!', reply_markup=await started_work_adm_kb(u=u))

        except Exception:
            await call.message.answer(text='Ish boshlandi!', reply_markup=await started_work_adm_kb(u=u))


@router.callback_query(F.data=='end_work', RoleFilter(roles=[1,2,3]))
async def end_work_cl(call: types.CallbackQuery):
    u = await vld(o=call, u=call.from_user)
    await DailyReportWorker.end(user_id=u.idn)
    datas = await Gadget.get_all(
        ex=f'AND worker={u.idn} AND is_stopped is False'
    )
    if len(datas) > 0:
        for data in datas:
            await stop_cl(call=call, idn=data.idn, redirect=False, auto_run=True)

    try:
        await call.message.edit_text(text='Ish tugatildi!', reply_markup=await menu_adm_kb())

    except Exception:
        await call.message.answer(text='Ish tugatildi!', reply_markup=await menu_adm_kb())
    return


@router.callback_query(F.data=='super_kb', RoleFilter(roles=[2]))
async def super_kb(call: types.CallbackQuery):
    await call.answer()
    await vld(o=call, u=call.from_user)

    try:
        await call.message.edit_text(text='⚙️ Super', reply_markup=await main_kb_su())

    except Exception:
        await call.message.answer(text='⚙️ Super', reply_markup=await main_kb_su())
    return


@router.callback_query(F.data=='others', RoleFilter(roles=[1,2,3]))
async def others_cl(call: types.CallbackQuery):
    await call.answer()
    u = await vld(o=call, u=call.from_user)

    try:
        await call.message.edit_text(text='⚙️ Boshqalar', reply_markup=await others_adm_kb(u=u))

    except Exception:
        await call.message.answer(text='⚙️ Boshqalar', reply_markup=await others_adm_kb(u=u))
    return


@router.callback_query(F.data.startswith("page_"))
async def page_callback(call: types.CallbackQuery):
    await call.answer()
    await vld(o=call, u=call.from_user)

    page = call.data.split("_")[1]
    type_data = call.data.split("_")[2]
    print("a"*200)
    print(page)
    print(type_data)

    if type_data == "my-jobs":
        await my_jobs_cl(call=call, page=int(page))

    elif type_data == "get-job":
        await get_work_cl(call=call, page=int(page))

    elif type_data == "get-job+2":
        await change_price_gadgets_cl(call=call, page=int(page))
