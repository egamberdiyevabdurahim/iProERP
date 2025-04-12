from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from loader import Model, User


async def menu_adm_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💎 Ishni boshlash", callback_data="start_work"),
        ],
        [
            InlineKeyboardButton(text="🗂 Oxirgi ishlarim", callback_data="last_done_works")
        ]
    ])
    return kb


async def started_work_adm_kb(u: User):
    if u.role == 3:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🪪 Ro'yxatga olish", callback_data="register_gadget")
            ],
            [
                InlineKeyboardButton(text="💤 Ish kunini tugatish", callback_data="end_work")
            ]
        ])

    elif u.role == 1:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="📑 Ishlarim", callback_data="unfinished_works_of_mine_1")
            ],
            [
                InlineKeyboardButton(text="📦 Yangi ish olish", callback_data="get_work_1")
            ],
            [
                InlineKeyboardButton(text="📚 Boshqalar", callback_data="others")
            ],
            [
                InlineKeyboardButton(text="💤 Ish kunini tugatish", callback_data="end_work")
            ]
        ])

    elif u.role == 2:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="💼 Super", callback_data="super_kb")
            ],
            [
                InlineKeyboardButton(text="🪪 Ro'yxatga olish", callback_data="register_gadget")
            ],
            [
                InlineKeyboardButton(text="📑 Ishlarim", callback_data="unfinished_works_of_mine_1")
            ],
            [
                InlineKeyboardButton(text="📦 Yangi ish olish", callback_data="get_work_1")
            ],
            [
                InlineKeyboardButton(text="📚 Boshqalar", callback_data="others")
            ],
            [
                InlineKeyboardButton(text="💤 Ish kunini tugatish", callback_data="end_work")
            ]
        ])
    else:
        kb = None
    return kb


async def others_adm_kb(u: User):
    if u.role != 2:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Nomi bilan qidirish", callback_data="gadget_from_name")
            ],
            [
                InlineKeyboardButton(text="🔍 ID bilan qidirish", callback_data="gadget_from_idn")
            ],
            [
                InlineKeyboardButton(text="🔍 IMEI1 bilan qidirish", callback_data="gadget_from_imei1")
            ],
            [
                InlineKeyboardButton(text="🔍 IMEI2 bilan qidirish", callback_data="gadget_from_imei2")
            ],
            [
                InlineKeyboardButton(text="🔍 S/N bilan qidirish", callback_data="gadget_from_sn")
            ],
            [
                InlineKeyboardButton(text='🔙 Ortga', callback_data='home')
            ],
        ])

    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔍 Nomi bilan qidirish", callback_data="gadget_from_name")
            ],
            [
                InlineKeyboardButton(text="🔍 ID bilan qidirish", callback_data="gadget_from_idn")
            ],
            [
                InlineKeyboardButton(text="🔍 IMEI1 bilan qidirish", callback_data="gadget_from_imei1")
            ],
            [
                InlineKeyboardButton(text="🔍 IMEI2 bilan qidirish", callback_data="gadget_from_imei2")
            ],
            [
                InlineKeyboardButton(text="🔍 S/N bilan qidirish", callback_data="gadget_from_sn")
            ],
            [
                InlineKeyboardButton(text="📊 Ishchilar pul bilan", callback_data="workers_by_money")
            ],
            [
                InlineKeyboardButton(text="📊 Ishchilar ish soni bilan", callback_data="workers_by_works")
            ],
            [
                InlineKeyboardButton(text="📊 Ishchilar umumiy", callback_data="workers_by_all")
            ],
            [
                InlineKeyboardButton(text='🔙 Ortga', callback_data='home')
            ],
        ])

    return kb


async def get_my_jobs_adm_kb(
        u,
        total_pages,
        current_gadgets,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()

    for gadget in current_gadgets:
        if gadget.is_stopped is False:
            markup.row(
                InlineKeyboardButton(
                    text=f"Ishladi ✅",
                    callback_data=f"works_{gadget.idn}"
                ),
                InlineKeyboardButton(
                    text=f"Ishlamadi ❌",
                    callback_data=f"not-works_{gadget.idn}"
                )
            )

        markup.add(
            InlineKeyboardButton(
                text=f"Batafsil ℹ️",
                callback_data=f"detailed_{gadget.idn}+unfinished_works_of_mine_1"
            )
        )
        if gadget.is_stopped is False:
            markup.add(
                InlineKeyboardButton(
                    text=f"Kechish ⏹️",
                    callback_data=f"lose_{gadget.idn}"
                )
            )
        markup.adjust(2)

        if gadget.is_stopped:
            markup.row(
                InlineKeyboardButton(
                    text=f"Davom etish ⏳",
                    callback_data=f"continue_{gadget.idn}"
                ),
                InlineKeyboardButton(
                    text=f"Narxini o'zgartirish 🔁",
                    callback_data=f"change-price_{gadget.idn}"
                )
            )

        else:
            markup.row(
                InlineKeyboardButton(
                    text=f"To'xtatish 🤚",
                    callback_data=f"stop_{gadget.idn}"
                ),
                InlineKeyboardButton(
                    text=f"Narxini o'zgartirish 🔁",
                    callback_data=f"change-price_{gadget.idn}"
                )
            )

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"page_{page - 1}_my-jobs"
            )
        )
    navigation_buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data='nothing'
        )
    )

    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"page_{page + 1}_my-jobs"
            )
        )

    markup.row(*navigation_buttons)
    markup.row(InlineKeyboardButton(text='🔙 Ortga', callback_data='home'))

    return markup.as_markup()


async def get_job_adm_kb(
        u,
        total_pages,
        current_gadgets,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()

    for gadget in current_gadgets:
        markup.add(
            InlineKeyboardButton(
                text=f"Ishni olish 🖇",
                callback_data=f"get-job_{gadget.idn}"
            )
        )
        markup.add(
            InlineKeyboardButton(
                text=f"Batafsil ℹ️",
                callback_data=f"detailed_{gadget.idn}+get_work_1"
            )
        )

    markup.adjust(1)
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"page_{page - 1}_get-job"
            )
        )
    navigation_buttons.append(
        InlineKeyboardButton(
            text=f"{page}/{total_pages}",
            callback_data='nothing'
        )
    )

    if page < total_pages:
        navigation_buttons.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"page_{page + 1}_get-job"
            )
        )

    markup.row(*navigation_buttons)
    markup.row(InlineKeyboardButton(text='🔙 Ortga', callback_data='home'))

    return markup.as_markup()


async def model_adm_kb():
    kb = ReplyKeyboardBuilder()
    model = await Model.get_heads()
    for m in model:
        kb.add(KeyboardButton(text=m.name))

    kb.adjust(2)
    kb.add(KeyboardButton(text="Bo'shqa"))
    return kb.as_markup(resize_keyboard=True)

async def color_adm_kb():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🖤 Qora", callback_data="🖤 Qora"),
            InlineKeyboardButton(text="🤍 Oq", callback_data="🤍 Oq"),
            InlineKeyboardButton(text="⚪ Kulrang", callback_data="⚪ Kulrang"),
        ],
        [
            InlineKeyboardButton(text="🏅 Oltin (Gold)", callback_data="🏅 Oltin (Gold)"),
            InlineKeyboardButton(text="💿 Kumush (Silver)", callback_data="💿 Kumush (Silver)"),
            InlineKeyboardButton(text="🥉 Bronza (Bronze)", callback_data="🥉 Bronza (Bronze)"),
        ],
        [
            InlineKeyboardButton(text="🌷 Atirgul Oltin (Rose Gold)", callback_data="🌷 Atirgul Oltin (Rose Gold)"),
            InlineKeyboardButton(text="🪨 Grafit (Graphite)", callback_data="🪨 Grafit (Graphite)"),
            InlineKeyboardButton(text="🟠 To‘q sariq", callback_data="🟠 To‘q sariq"),
        ],
        [
            InlineKeyboardButton(text="🔵 Ko‘k", callback_data="🔵 Ko‘k"),
            InlineKeyboardButton(text="🟢 Yashil", callback_data="🟢 Yashil"),
            InlineKeyboardButton(text="🔴 Qizil", callback_data="🔴 Qizil"),
        ],
        [
            InlineKeyboardButton(text="🟣 Binafsha", callback_data="🟣 Binafsha"),
            InlineKeyboardButton(text="🎀 Pushti", callback_data="🎀 Pushti"),
            InlineKeyboardButton(text="💛 Sariq", callback_data="💛 Sariq"),
        ],
    ])
    return kb


async def gadget_search_name_data_kb(
        text,
        current_gadgets,
        total_pages,
        start_index,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()
    page = int(page)

    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"detailed_{gadget.idn}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search-name_{text}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='nothing'))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search-name_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='🔙 '+'Ortga', callback_data='others'))

    return markup.as_markup()


async def gadget_search_idn_data_kb(
        text,
        current_gadgets,
        total_pages,
        start_index,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()
    page = int(page)

    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"detailed_{gadget.idn}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search-idn_{text}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='nothing'))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search-idn_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='🔙 '+'Ortga', callback_data='others'))

    return markup.as_markup()


async def gadget_search_sn_data_kb(
        text,
        current_gadgets,
        total_pages,
        start_index,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()
    page = int(page)

    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"detailed_{gadget.idn}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search-sn_{text}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='nothing'))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search-sn_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='🔙 '+'Ortga', callback_data='others'))

    return markup.as_markup()


async def gadget_search_imei1_data_kb(
        text,
        current_gadgets,
        total_pages,
        start_index,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()
    page = int(page)

    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"detailed_{gadget.idn}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search-imei1_{text}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='nothing'))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search-imei1_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='🔙 '+'Ortga', callback_data='others'))

    return markup.as_markup()


async def gadget_search_imei2_data_kb(
        text,
        current_gadgets,
        total_pages,
        start_index,
        page=1,
        page_size=10
):
    markup = InlineKeyboardBuilder()
    page = int(page)

    counter = start_index
    for gadget in current_gadgets:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"detailed_{gadget.idn}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search-imei2_{text}"))
    navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data='nothing'))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search-imei2_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='🔙 '+'Ortga', callback_data='others'))

    return markup.as_markup()
