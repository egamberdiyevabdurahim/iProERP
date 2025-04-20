import re

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from buttons.admin import gadget_search_idn_data_kb, gadget_search_sn_data_kb, gadget_search_imei1_data_kb, \
    gadget_search_imei2_data_kb, gadget_search_name_data_kb
from filters.role import RoleFilter
from loader import Gadget, Model
from states.admin import FindGadgetBySt
from utils.validator import vld

router = Router()


@router.callback_query(F.data == "gadget_from_name", RoleFilter([1,2,3]))
async def find_gadget_by_name_cl(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)
    await call.message.edit_text("Gatgetni Nomini kiriting:")
    await state.set_state(FindGadgetBySt.name)


@router.message(FindGadgetBySt.name)
async def find_gadget_by_name_m(message: types.Message,
                                page=1, page_size=10,
                                text=None, user=None):
    if user is None:
        user = message.from_user

    await vld(o=message, u=user)
    if text is None:
        text = message.text

    gadgets = await Gadget.get_by_search_name(search_query=text)

    total_gadgets = len(gadgets)
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{text} - "+"Gadgetlar"+":\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_gadgets = gadgets[start_index:end_index]

    # Add gadget buttons
    counter = start_index
    for gadget in current_gadgets:
        model = await Model.get_data(idn=gadget.model)
        counter += 1
        idn = model.name + ' ' + gadget.name
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        highlighted_title = pattern.sub(r"<u><b>\g<0></b></u>", idn)

        text_data += f"{counter}. {highlighted_title}\n"

    try:
        await message.edit_text(text=text_data,
                                reply_markup=await gadget_search_name_data_kb(
                                    text=text,
                                    page=page,
                                    page_size=page_size,
                                    current_gadgets=current_gadgets,
                                    total_pages=total_pages,
                                    start_index=start_index
                                ), parse_mode='HTML')

    except Exception:
        await message.answer(text=text_data,
                             reply_markup=await gadget_search_name_data_kb(
                                 text=text,
                                 page=page,
                                 page_size=page_size,
                                 current_gadgets=current_gadgets,
                                 total_pages=total_pages,
                                 start_index=start_index
                             ), parse_mode='HTML')


@router.callback_query(F.data == "gadget_from_idn", RoleFilter([1,2,3]))
async def find_gadget_by_idn_cl(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)
    await call.message.edit_text("Gatgetni ID-ni kiriting:")
    await state.set_state(FindGadgetBySt.idn)


@router.message(FindGadgetBySt.idn)
async def find_gadget_by_idn_m(message: types.Message,
                                   page=1, page_size=10,
                                   text=None, user=None):
    if user is None:
        user = message.from_user

    await vld(o=message, u=user)
    if text is None:
        text = message.text

    gadgets = await Gadget.get_by_search_idn(search_query=text)

    total_gadgets = len(gadgets)
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{text} - "+"Gadgetlar"+":\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_gadgets = gadgets[start_index:end_index]

    # Add gadget buttons
    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        idn = str(gadget.idn)
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        highlighted_title = pattern.sub(r"<u><b>\g<0></b></u>", idn)

        text_data += f"{counter}. {highlighted_title}\n"

    try:
        await message.edit_text(text=text_data,
                                reply_markup=await gadget_search_idn_data_kb(
                                    text=text,
                                    page=page,
                                    page_size=page_size,
                                    current_gadgets=current_gadgets,
                                    total_pages=total_pages,
                                    start_index=start_index
                                ), parse_mode='HTML')

    except Exception:
        await message.answer(text=text_data,
                             reply_markup=await gadget_search_idn_data_kb(
                                 text=text,
                                 page=page,
                                 page_size=page_size,
                                 current_gadgets=current_gadgets,
                                 total_pages=total_pages,
                                 start_index=start_index
                             ), parse_mode='HTML')


@router.callback_query(F.data == "gadget_from_sn", RoleFilter([1,2,3]))
async def find_gadget_by_sn_cl(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)
    await call.message.edit_text("Gatgetni S/N-sini kiriting:")
    await state.set_state(FindGadgetBySt.serial_number)


@router.message(FindGadgetBySt.serial_number)
async def find_gadget_by_sn_m(message: types.Message,
                                   page=1, page_size=10,
                                   text=None, user=None):
    if user is None:
        user = message.from_user

    await vld(o=message, u=user)
    if text is None:
        text = message.text

    gadgets = await Gadget.get_by_search_sn(search_query=text)

    total_gadgets = len(gadgets)
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{text} - "+"Gadgetlar"+":\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_gadgets = gadgets[start_index:end_index]

    # Add gadget buttons
    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        sn = gadget.serial_number
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        highlighted_title = pattern.sub(r"<u><b>\g<0></b></u>", sn)

        text_data += f"{counter}. {highlighted_title}\n"

    try:
        await message.edit_text(text=text_data,
                                reply_markup=await gadget_search_sn_data_kb(
                                    text=text,
                                    page=page,
                                    page_size=page_size,
                                    current_gadgets=current_gadgets,
                                    total_pages=total_pages,
                                    start_index=start_index
                                ), parse_mode='HTML')

    except Exception:
        await message.answer(text=text_data,
                             reply_markup=await gadget_search_sn_data_kb(
                                 text=text,
                                 page=page,
                                 page_size=page_size,
                                 current_gadgets=current_gadgets,
                                 total_pages=total_pages,
                                 start_index=start_index
                             ), parse_mode='HTML')


@router.callback_query(F.data == "gadget_from_imei1", RoleFilter([1,2,3]))
async def find_gadget_by_imei1_cl(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)
    await call.message.edit_text("Gatgetni IMEI1-ni kiriting:")
    await state.set_state(FindGadgetBySt.imei1)


@router.message(FindGadgetBySt.imei1)
async def find_gadget_by_imei1_m(message: types.Message,
                                   page=1, page_size=10,
                                   text=None, user=None):
    if user is None:
        user = message.from_user

    await vld(o=message, u=user)
    if text is None:
        text = message.text

    gadgets = await Gadget.get_by_search_imei1(search_query=text)

    total_gadgets = len(gadgets)
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{text} - "+"Gadgetlar"+":\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_gadgets = gadgets[start_index:end_index]

    # Add gadget buttons
    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        imei1 = gadget.imei1
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        highlighted_title = pattern.sub(r"<u><b>\g<0></b></u>", imei1)

        text_data += f"{counter}. {highlighted_title}\n"

    try:
        await message.edit_text(text=text_data,
                                reply_markup=await gadget_search_imei1_data_kb(
                                    text=text,
                                    page=page,
                                    page_size=page_size,
                                    current_gadgets=current_gadgets,
                                    total_pages=total_pages,
                                    start_index=start_index
                                ), parse_mode='HTML')

    except Exception:
        await message.answer(text=text_data,
                             reply_markup=await gadget_search_imei1_data_kb(
                                 text=text,
                                 page=page,
                                 page_size=page_size,
                                 current_gadgets=current_gadgets,
                                 total_pages=total_pages,
                                 start_index=start_index
                             ), parse_mode='HTML')


@router.callback_query(F.data == "gadget_from_imei2", RoleFilter([1,2,3]))
async def find_gadget_by_imei2_cl(call: types.CallbackQuery, state: FSMContext):
    await vld(o=call, u=call.from_user)
    await call.message.edit_text("Gatgetni IMEI2-ni kiriting:")
    await state.set_state(FindGadgetBySt.imei2)


@router.message(FindGadgetBySt.imei2)
async def find_gadget_by_imei2_m(message: types.Message,
                                   page=1, page_size=10,
                                   text=None, user=None):
    if user is None:
        user = message.from_user

    await vld(o=message, u=user)
    if text is None:
        text = message.text

    gadgets = await Gadget.get_by_search_imei1(search_query=text)

    total_gadgets = len(gadgets)
    page_size = int(page_size)
    total_pages = (total_gadgets + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{text} - "+"Gadgetlar"+":\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_gadgets = gadgets[start_index:end_index]

    # Add gadget buttons
    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        imei2 = gadget.imei2
        pattern = re.compile(re.escape(text), re.IGNORECASE)
        highlighted_title = pattern.sub(r"<u><b>\g<0></b></u>", imei2)

        text_data += f"{counter}. {highlighted_title}\n"

    try:
        await message.edit_text(text=text_data,
                                reply_markup=await gadget_search_imei2_data_kb(
                                    text=text,
                                    page=page,
                                    page_size=page_size,
                                    current_gadgets=current_gadgets,
                                    total_pages=total_pages,
                                    start_index=start_index
                                ), parse_mode='HTML')

    except Exception:
        await message.answer(text=text_data,
                             reply_markup=await gadget_search_imei2_data_kb(
                                 text=text,
                                 page=page,
                                 page_size=page_size,
                                 current_gadgets=current_gadgets,
                                 total_pages=total_pages,
                                 start_index=start_index
                             ), parse_mode='HTML')
