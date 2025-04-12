import os
import string
from datetime import datetime

import pytz


PATTERN = r"^\+?[\d\s]{10,15}$"
BASE62_ALPHABET = string.digits + string.ascii_uppercase + string.ascii_lowercase

ADMIN_LINK = "@MasterPhoneAdmin"
ADMIN_EMAIL = "egamberdiyevabdurahim@gmail.com"

# Setting the base path
BASE_PATH = os.path.dirname(__file__)


tashkent_timezone = pytz.timezone("Asia/Tashkent")
def tas_t():
    return datetime.now(tashkent_timezone)
