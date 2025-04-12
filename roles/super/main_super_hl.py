from aiogram import types, Router, F

from buttons.super import user_mng_kb_su, gadget_mng_kb_su
from filters.role import RoleFilter
from utils.validator import vld

router = Router()


@router.callback_query(F.data=='user_mng', RoleFilter(roles=[2]))
async def user_mng_kb(call: types.CallbackQuery):
    await call.answer()
    u = await vld(o=call, u=call.from_user)

    try:
        await call.message.edit_text(text='⚙ User boshqaruvi', reply_markup=await user_mng_kb_su())

    except Exception:
        await call.message.answer(text='⚙ User boshqaruvi', reply_markup=await user_mng_kb_su())
    return


@router.callback_query(F.data=='gadget_mng', RoleFilter(roles=[2]))
async def gadget_mng_kb(call: types.CallbackQuery):
    await call.answer()
    u = await vld(o=call, u=call.from_user)

    try:
        await call.message.edit_text(text='⚙ Gadget boshqaruvi', reply_markup=await gadget_mng_kb_su())

    except Exception:
        await call.message.answer(text='⚙ Gadget boshqaruvi', reply_markup=await gadget_mng_kb_su())
    return