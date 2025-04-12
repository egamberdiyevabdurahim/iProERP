from aiogram.types.input_file import FSInputFile

from loader import bot, User
from utils.logger import error_logger


async def send_m(
        u,
        ms = None,
        rep_mark = None,
        img = None,
        vid = None,
        media_group = None,
        doc = None,
        with_input = None,
        prt = None,
        prs_mode = None,
        with_spoiler = None,
        txt_above = None,
        count = 1
):
    if isinstance(u, User):
        chat_id = u.chat_id
    else:
        chat_id = u.id

    try:
        if img:
            if with_input:
                img = FSInputFile(img)
            await bot.send_photo(
                photo=img,
                caption=ms,
                protect_content=prt,
                reply_markup=rep_mark,
                chat_id=chat_id,
                has_spoiler=with_spoiler,
                show_caption_above_media=txt_above
            )

        elif vid:
            if with_input:
                vid = FSInputFile(vid)

            await bot.send_video(
                video=vid,
                caption=ms,
                protect_content=prt,
                reply_markup=rep_mark,
                chat_id=chat_id,
                has_spoiler=with_spoiler,
                show_caption_above_media=txt_above
            )

        elif doc:
            if with_input:
                doc = FSInputFile(doc)

            await bot.send_document(
                document=doc,
                caption=ms,
                protect_content=prt,
                reply_markup=rep_mark,
                chat_id=chat_id
            )

        # Handle sending a media group
        elif media_group:
            try:
                if rep_mark:
                    await bot.send_media_group(media=media_group, protect_content=prt, chat_id=chat_id)
                    await bot.send_m(chat_id=chat_id, ms=ms, protect_content=prt, rep_mark=rep_mark)

                elif ms and not rep_mark:
                    media_group = media_group[0].caption=ms
                    await bot.send_media_group(media=media_group, protect_content=prt, chat_id=chat_id)

                else:
                    await bot.send_media_group(media=media_group, protect_content=prt, chat_id=chat_id)

            except Exception:
                pass

        # Handle sending plain text
        elif ms:
            await bot.send_m(ms=ms, protect_content=prt, rep_mark=rep_mark, chat_id=chat_id)

    except Exception as e:
        if count < 3:  # Retry sending the obj up to 3 times
            await send_m(
                u,
                ms,
                rep_mark,
                img,
                vid,
                media_group,
                doc,
                with_input,
                prt,
                prs_mode,
                with_spoiler,
                txt_above,
                count + 1
            )

        else:
            await error_logger(u_idn=chat_id, description=e, error_pl="send_message")
            return None
