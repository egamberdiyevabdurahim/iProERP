from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from filters.role import RoleFilter
from loader import User, Account
from states.admin import RegisterSt, DeleteSt
from utils.validator import vld

router = Router()


@router.callback_query(F.data=="new_user", RoleFilter([2]))
async def new_user(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)

    await call.message.answer(text="Chat id yuboring:")
    await state.set_state(RegisterSt.chat_id)


@router.message(RegisterSt.chat_id)
async def register_chat_id(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    chat_id = message.text

    if chat_id.isnumeric():
        await state.update_data(chat_id=chat_id)
        await message.answer(text="Role ni kiriting\n1: Ishchi, 3: Ro'yxatchi")
        await state.set_state(RegisterSt.role)

    else:
        await message.answer(text="Chat id xato")
        await state.clear()


@router.message(RegisterSt.role)
async def register_role(message: types.Message, state: FSMContext):
    u = await vld(o=message, u=message.from_user)
    role = int(message.text)

    if role in [1, 3]:
        state_data = await state.get_data()
        chat_id = state_data.get('chat_id')

        await Account.create(
            chat_id=chat_id,
            role=role,
            created_by=u.idn
        )
        await message.answer(text="Tayyor endi botga /start bersa bo'ldi ✅")
        await state.clear()

    else:
        await message.answer(text="Role xato")
        await state.clear()


@router.callback_query(F.data=="delete_user", RoleFilter([2]))
async def delete_user(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)

    await call.message.answer(text="Chat id yuboring:")
    await state.set_state(DeleteSt.chat_id)


@router.message(DeleteSt.chat_id)
async def delete_chat_id(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    chat_id = message.text
    if chat_id.isnumeric():
        await User.delete(chat_id=chat_id)
        await Account.delete(chat_id=chat_id)
        await message.answer(text="Tayyor ✅")

    else:
        await message.answer(text="Chat id xato")
        await state.clear()
