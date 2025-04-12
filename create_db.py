import asyncio


from loader import User, DailyReportWorker, Errors, History, GadgetWorkers, GadgetPhoto, Gadget, Model, Account

asyncio.run(Account.create_table())
asyncio.run(User.create_table())
asyncio.run(Model.create_table())
asyncio.run(Gadget.create_table())
asyncio.run(GadgetPhoto.create_table())
asyncio.run(GadgetWorkers.create_table())
asyncio.run(History.create_table())
asyncio.run(Errors.create_table())
asyncio.run(DailyReportWorker.create_table())

asyncio.run(User.create(
    chat_id=2139292627,
    tg_username="MasterPhoneAdmin",
    first_name="MasterPhone",
    role=2
))

asyncio.run(User.create(
    chat_id=366694338,
    tg_username="iProServis",
    first_name="iProServis",
    role=2
))