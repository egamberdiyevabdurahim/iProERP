from aiogram.fsm.state import StatesGroup, State


class RegisterGadgetState(StatesGroup):
    model = State()
    new_model = State()
    seria = State()
    name = State()
    client_name = State()
    client_phone_number = State()
    client = State()
    imei1 = State()
    imei2 = State()
    serial_number = State()
    color = State()
    price = State()
    description = State()
    images = State()
    end = State()


class RegisterSt(StatesGroup):
    chat_id = State()
    role = State()


class DeleteSt(StatesGroup):
    chat_id = State()


class WorksSt(StatesGroup):
    idn = State()
    expense = State()


class NotWorksSt(StatesGroup):
    idn = State()
    expense = State()


class ChangePriceSt(StatesGroup):
    idn = State()
    price = State()


class FindGadgetBySt(StatesGroup):
    name = State()
    idn = State()
    imei1 = State()
    imei2 = State()
    serial_number = State()


class SearchBySt(StatesGroup):
    type_data = State()
    text = State()
