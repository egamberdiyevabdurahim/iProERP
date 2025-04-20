from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, InputMediaPhoto

from buttons.admin import model_adm_kb
from buttons.main import skip_kb_kb
from database_config.config import MOVIE_DATA_GROUP_ID
from filters.role import RoleFilter
from loader import User, Gadget, GadgetPhoto, bot, Model
from roles.admin.main_adm_hl import start_work_cl
from states.admin import RegisterGadgetState, RegisterGadget2State
from utils.algorithm import generate_barcode
from utils.validator import vld

router = Router()


@router.callback_query(F.data=='register_gadget', RoleFilter([2,3]))
async def register_gadget_cl(call: types.CallbackQuery, state=FSMContext):
    await vld(o=call, u=call.from_user, delete=True)
    await call.message.answer(text='Modelini tanlang:', reply_markup=await model_adm_kb())
    await state.set_state(RegisterGadgetState.model)


@router.message(RegisterGadgetState.model)
async def register_gadget_model_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    model = await Model.get_by_name(message.text.strip())
    if message.text.strip() == "Bo'shqa":
        await message.answer(text='Yangi model nomini kiriting:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterGadgetState.new_model)

    elif model is None:
        await message.answer(text='Xato narsa kiritildi!', reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    await state.update_data(model=model.idn)
    await message.answer(text='Nomini kiriting:', reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegisterGadgetState.name)


@router.message(RegisterGadgetState.new_model)
async def register_gadget_new_model_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await Model.create(name=message.text.strip())
    model = await Model.get_by_name(message.text.strip())

    await message.answer(text="Yangi model qo'shildi!")
    await state.update_data(model=model.idn)

    await message.answer(text='Nomini kiriting:')
    await state.set_state(RegisterGadgetState.name)


@router.message(RegisterGadgetState.name)
async def register_gadget_name_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await message.answer(text='Mijoz ismini kiriting:', reply_markup=await skip_kb_kb())
    await state.update_data(name=message.text.strip())
    await state.set_state(RegisterGadgetState.client_name)


@router.message(RegisterGadgetState.client_name)
async def register_gadget_client_name_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    client_name = message.text.strip()
    if client_name == "O'tkazib yuborish":
        client_name = None
    await message.answer(text='Mijoz raqamini kiriting:', reply_markup=await skip_kb_kb())
    await state.update_data(client_name=client_name)
    await state.set_state(RegisterGadgetState.client_phone_number)


@router.message(RegisterGadgetState.client_phone_number)
async def register_gadget_client_phone_number_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    client_number = message.text.strip()
    if client_number == "O'tkazib yuborish":
        client_number = None
    await message.answer(text='IMEI1 ni kiriting:', reply_markup=await skip_kb_kb())
    await state.update_data(client_phone_number=client_number)
    await state.set_state(RegisterGadgetState.imei1)


@router.message(RegisterGadgetState.imei1)
async def register_gadget_imei1_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    imei1 = message.text.strip()
    if imei1 == "O'tkazib yuborish":
        imei1 = None
    await message.answer(text='IMEI2 ni kiriting:', reply_markup=await skip_kb_kb())
    await state.update_data(imei1=imei1)
    await state.set_state(RegisterGadgetState.imei2)


@router.message(RegisterGadgetState.imei2)
async def register_gadget_imei2_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    imei2 = message.text.strip()
    if imei2 == "O'tkazib yuborish":
        imei2 = None
    await message.answer(text='S/N kiriting:', reply_markup=await skip_kb_kb())
    await state.update_data(imei2=imei2)
    await state.set_state(RegisterGadgetState.serial_number)


@router.message(RegisterGadgetState.serial_number)
async def register_gadget_serial_number_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    sn = message.text.strip()
    if sn == "O'tkazib yuborish":
        sn = None
    await message.answer(text='Narxini kiriting:', reply_markup=ReplyKeyboardRemove())
    await state.update_data(serial_number=sn)
    await state.set_state(RegisterGadgetState.price)


@router.message(RegisterGadgetState.price)
async def register_gadget_price_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await message.answer(text='Batafsil kiriting:', reply_markup=ReplyKeyboardRemove())
    await state.update_data(price=message.text)
    await state.set_state(RegisterGadgetState.description)


@router.message(RegisterGadgetState.description)
async def register_gadget_description_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await message.answer(text='Rasmlar yuboring:')
    await state.update_data(description=message.text.strip())
    await state.set_state(RegisterGadgetState.images)


@router.message(RegisterGadgetState.images)
async def register_gadget_photo_ms(message: types.Message, state: FSMContext):
    if message.photo:
        media_items = message.photo
        highest_quality_photo = media_items[-1]
        file_id = highest_quality_photo.file_id

        data = await state.get_data()
        if 'images' in data:
            data['images'].append(file_id)
        else:
            data['images'] = [file_id]

        await state.update_data(images=data['images'])
        await message.answer(text="Rasm qo'shildi. Yana yuboring yoki tugatish uchun done jo'nating!")

    elif message.text.lower() == 'done':
        data = await state.get_data()
        await state.clear()
        await register_gadget_end_ms(message, data)

    else:
        await message.answer(text="Iltimos rasm jo'nating yoki tugatish uchun done yuboring!")


@router.message(RegisterGadgetState.end)
async def register_gadget_end_ms(message: types.Message, data):
    user = await User.get_data(message.from_user.id)

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    imei1 = data.get('imei1')
    imei2 = data.get('imei2')
    model = data.get('model')
    serial_number = data.get('serial_number')
    color = data.get('color')
    client_name = data.get('client_name')
    client_phone_number = data.get('client_phone_number')
    images = data.get('images')

    gadget = await Gadget.create(
        hash_idn=None,
        qr_code=None,
        br_code=None,
        name=name,
        description=description,
        price=price,
        imei1=imei1,
        imei2=imei2,
        model=model,
        serial_number=serial_number,
        color=color,
        client=None,
        client_name=client_name,
        client_phone_number=client_phone_number,
        client_chat_id=None,
        created_by=user.idn
    )

    num = gadget.idn
    bio = generate_barcode(num)

    for photo in images:
        await GadgetPhoto.create(
            gadget=gadget.idn,
            photo=photo
        )
    model_name = await Model.get_data(model)

    caption = f"<b>ID</b>: {num}\n"\
              f"<b>Modeli</b>: {model_name.name}\n"\
              f"<b>Nomi</b>: {name}\n"\
              f"<b>Narxi</b>: {price}\n"\
              f"<b>IMEI</b>: {imei1}/{imei2}\n"\
              f"<b>S/N</b>: {serial_number}\n"\
              f"<b>Mijoz ismi</b>: {client_name}\n"\
              f"<b>Mijoz nomeri</b>: {client_phone_number}\n"

    await message.answer(text=f"{data.get('name')} - Muvaffaqiyatli registratsiya buldi!")
    medias = []
    for media in images:
        medias.append(InputMediaPhoto(media=media))

    await bot.send_media_group(
        media=medias,
        chat_id=MOVIE_DATA_GROUP_ID,
    )
    sent_photo = await bot.send_photo(
        chat_id=MOVIE_DATA_GROUP_ID,
        caption=caption,
        photo=bio,
        parse_mode='HTML',
    )
    br_idn = sent_photo.photo[-1].file_id
    await Gadget.column_updater(
        idn=num,
        col_name='br_code',
        data=br_idn,
        updater=user.idn
    )

    await start_work_cl(call=message, u=message.from_user)


@router.callback_query(F.data=='register_gadget2', RoleFilter([2,3]))
async def register_gadget2_cl(call: types.CallbackQuery, state=FSMContext):
    await vld(o=call, u=call.from_user, delete=True)
    await call.message.answer(text='Modelini tanlang:', reply_markup=await model_adm_kb())
    await state.set_state(RegisterGadget2State.model)


@router.message(RegisterGadget2State.model)
async def register_gadget2_model_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    model = await Model.get_by_name(message.text.strip())
    if message.text.strip() == "Bo'shqa":
        await message.answer(text='Yangi model nomini kiriting:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(RegisterGadget2State.new_model)

    elif model is None:
        await message.answer(text='Xato narsa kiritildi!', reply_markup=ReplyKeyboardRemove())
        return await state.clear()

    await state.update_data(model=model.idn)
    text1 = ("IMEI 1 dona kiritsangizham bo'ladi yani IMEI1 ga S/N ham muxim emas. "
             "Lekin IMEI 1 ta bo'lsaham kiritilishi kerak. Mijoz ismi kiritilmasaham bo'ladi, "
             "Mijoz raqami kiritilmasaham bo'ladi. Lekin ikkovisidan 1 ni kiritish kerak. "
             "Forma o'zgarmasin va textda ^ - shu belgidan FOYDALANILMASIN!\n\n")
    await message.answer(text=text1, reply_markup=ReplyKeyboardRemove())
    text = """
Nomi^
Mijoz ismi^
Mijoz raqami^
IMEI1^
IMEI2^
S/N^
Narx^
Qo'shimcha^
"""
    await message.answer(text=text, parse_mode='HTML')
    await state.set_state(RegisterGadget2State.full)


@router.message(RegisterGadget2State.new_model)
async def register_gadget2_new_model_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await Model.create(name=message.text.strip())
    model = await Model.get_by_name(message.text.strip())

    await message.answer(text="Yangi model qo'shildi!")
    await state.update_data(model=model.idn)

    text1 = ("IMEI 1 dona kiritsangizham bo'ladi yani IMEI1 ga S/N ham muxim emas. "
             "Lekin IMEI 1 ta bo'lsaham kiritilishi kerak. Mijoz ismi kiritilmasaham bo'ladi, "
             "Mijoz raqami kiritilmasaham bo'ladi. Lekin ikkovisidan 1 ni kiritish kerak. "
             "Forma o'zgarmasin va textda ^ - shu belgidan FOYDALANILMASIN!\n\n")
    await message.answer(text=text1, reply_markup=ReplyKeyboardRemove())
    text = """
Nomi^
Mijoz ismi^
Mijoz raqami^
IMEI1^
IMEI2^
S/N^
Narx^
Qo'shimcha^
    """
    await message.answer(text=text, parse_mode='HTML')
    await state.set_state(RegisterGadget2State.full)


@router.message(RegisterGadget2State.full)
async def register_gadget2_full_ms(message: types.Message, state: FSMContext):
    await vld(o=message, u=message.from_user)
    await message.answer(text='Rasmlar yuboring:')
    await state.update_data(full=message.text)
    await state.set_state(RegisterGadget2State.images)


@router.message(RegisterGadget2State.images)
async def register_gadget2_photo_ms(message: types.Message, state: FSMContext):
    if message.photo:
        media_items = message.photo
        highest_quality_photo = media_items[-1]
        file_id = highest_quality_photo.file_id

        data = await state.get_data()
        if 'images' in data:
            data['images'].append(file_id)
        else:
            data['images'] = [file_id]

        await state.update_data(images=data['images'])
        await message.answer(text="Rasm qo'shildi. Yana yuboring yoki tugatish uchun done jo'nating!")

    elif message.text.lower() == 'done':
        data = await state.get_data()
        await state.clear()
        await register_gadget2_end_ms(message, data)

    else:
        await message.answer(text="Iltimos rasm jo'nating yoki tugatish uchun done yuboring!")


@router.message(RegisterGadget2State.end)
async def register_gadget2_end_ms(message: types.Message, data):
    user = await User.get_data(message.from_user.id)

    full = data.get('full')
    text = full.strip().split('\n')
    d = {}
    for i in text:
        i = i.split('^')
        if len(i) > 1:
            d[i[0]] = i[-1]
    name = d.get('Nomi')
    description = data.get("Qo'shimcha")
    price = data.get('Narx')
    imei1 = data.get('IMEI1')
    imei2 = data.get('IMEI2')
    serial_number = data.get('S/N')
    client_name = data.get('Mijoz ismi')
    client_phone_number = data.get('Mijoz raqami')

    model = data.get('model')
    images = data.get('images')

    gadget = await Gadget.create(
        hash_idn=None,
        qr_code=None,
        br_code=None,
        name=name,
        description=description,
        price=price,
        imei1=imei1,
        imei2=imei2,
        model=model,
        serial_number=serial_number,
        client_name=client_name,
        client_phone_number=client_phone_number,
        created_by=user.idn
    )

    num = gadget.idn
    bio = generate_barcode(num)

    for photo in images:
        await GadgetPhoto.create(
            gadget=gadget.idn,
            photo=photo
        )
    model_name = await Model.get_data(model)

    caption = f"<b>ID</b>: {num}\n"\
              f"<b>Modeli</b>: {model_name.name}\n"\
              f"<b>Nomi</b>: {name}\n"\
              f"<b>Narxi</b>: {price}\n"\
              f"<b>IMEI</b>: {imei1}/{imei2}\n"\
              f"<b>S/N</b>: {serial_number}\n"\
              f"<b>Mijoz ismi</b>: {client_name}\n"\
              f"<b>Mijoz nomeri</b>: {client_phone_number}\n"

    await message.answer(text=f"{data.get('name')} - Muvaffaqiyatli registratsiya buldi!")
    medias = []
    for media in images:
        medias.append(InputMediaPhoto(media=media))

    await bot.send_media_group(
        media=medias,
        chat_id=MOVIE_DATA_GROUP_ID,
    )
    sent_photo = await bot.send_photo(
        chat_id=MOVIE_DATA_GROUP_ID,
        caption=caption,
        photo=bio,
        parse_mode='HTML',
    )
    br_idn = sent_photo.photo[-1].file_id
    await Gadget.column_updater(
        idn=num,
        col_name='br_code',
        data=br_idn,
        updater=user.idn
    )

    await start_work_cl(call=message, u=message.from_user)
