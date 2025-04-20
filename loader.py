from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.utils.i18n import I18n

from database_config.config import TOKEN
from models import history, errors, user, gadget, gadget_photo, daily_report_worker
from models.account import AccountModel
from models.gadget_workers import GadgetWorkersModel
from models.model import ModelModel

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# i18n = I18n(path="locales", default_locale="uz", domain="lang")
# _ = i18n.gettext

# MODELS
Account = AccountModel
User = user.UserModel
Model = ModelModel
Gadget = gadget.GadgetModel
GadgetPhoto = gadget_photo.GadgetPhotoModel
GadgetWorkers = GadgetWorkersModel
History = history.HistoryModel
Errors = errors.ErrorsModel
DailyReportWorker = daily_report_worker.DailyReportWorkerModel
