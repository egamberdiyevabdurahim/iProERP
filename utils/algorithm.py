import io
import barcode
from aiogram.types import BufferedInputFile
from barcode.writer import ImageWriter


def generate_barcode(idn):
    barcode_type = barcode.get_barcode_class("code128")  # Supports variable length
    br_code = barcode_type(str(idn), writer=ImageWriter())

    bio = io.BytesIO()
    br_code.write(bio)

    bio.seek(0)  # Kursorni boshiga qaytarish

    pho = BufferedInputFile(bio.getvalue(), filename="barcode.png")  # Aiogram 3.x uchun
    return pho
