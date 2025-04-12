from aiogram import types, Router, F
from aiogram.types import InputMediaPhoto

from filters.role import RoleFilter
from loader import Gadget, Model, GadgetPhoto, bot
from utils.message_deleter import message_deleter
from utils.validator import vld

router = Router()


@router.callback_query(F.data.startswith('detailed_'), RoleFilter([1, 2, 3]))
async def detailed_cl(
        call: types.CallbackQuery | types.Message,
        idn=None
):
    await vld(o=call, u=call.from_user)
    if not idn:
        idn = call.data.split("_")[1]
        idn = idn.split("+")[0]
        # link = call.data.split("+")[1]

    else:
        await message_deleter(u_id=call.from_user.id, message_id=call.message_id-1)
        await message_deleter(u_id=call.from_user.id, message_id=call.message_id)

    data = await Gadget.get_data(idn=idn)
    model = await Model.get_data(idn=data.model)
    images = await GadgetPhoto.get_by_gadget(gadget=idn)
    text = (
        f"<b>ID</b>: {idn}\n"
        f"<b>Modeli</b>: {model.name}\n"
        f"<b>Nomi</b>: {data.name}\n"
        f"<b>IMEI</b>: {data.imei1} | {data.imei2}\n"
        f"<b>S/N</b>: {data.serial_number}\n"
        f"<b>Mijoz</b>: {data.client_name}\n"
        f"<b>Telefon raqam</b>: {data.client_phone_number}\n"
        f"<b>Narxi</b>: {data.price}\n"
        f"<b>Yana</b>: {data.description}"
    )

    photos = [InputMediaPhoto(media=data.br_code, caption=text, parse_mode='HTML')]
    for image in images:
        photos.append(InputMediaPhoto(media=image.photo))

    await bot.send_media_group(
        media=photos,
        chat_id=call.from_user.id
    )
