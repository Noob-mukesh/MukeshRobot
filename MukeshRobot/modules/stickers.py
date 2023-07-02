import math
import os
import urllib.request as urllib
from html import escape
import textwrap
from html import escape
from urllib.parse import quote as urlquote

import cv2
import ffmpeg
from bs4 import BeautifulSoup
from cloudscraper import CloudScraper
import requests
from bs4 import BeautifulSoup as bs
from PIL import Image
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    TelegramError,
    Update,
)
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from MukeshRobot import dispatcher
from MukeshRobot.modules.disable import DisableAbleCommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="

def convert_gif(input):
    """ғᴜɴᴄᴛɪᴏɴ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴍᴘ4 ᴛᴏ ᴡᴇʙᴍ(ᴠᴘ9)!(ᴀʙɪsʜɴᴏɪ)"""

    vid = cv2.VideoCapture(input)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

    # check height and width to scale
    if width > height:
        width = 512
        height = -1
    elif height > width:
        height = 512
        width = -1
    elif width == height:
        width = 512
        height = 512

    converted_name = "kangsticker.webm"

    (
        ffmpeg.input(input)
        .filter("fps", fps=30, round="up")
        .filter("scale", width=width, height=height)
        .trim(start="00:00:00", end="00:00:03", duration="3")
        .output(
            converted_name,
            vcodec="libvpx-vp9",
            **{
                #'vf': 'scale=512:-1',
                "crf": "30"
            },
        )
        .overwrite_output()
        .run()
    )

    return converted_name
def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "Hey "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", The sticker id you are replying is :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Hello "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ɪᴅ sᴛɪᴄᴋᴇʀ",
            parse_mode=ParseMode.HTML,
        )
scraper = CloudScraper()


def get_cbs_data(query, page, user_id):
    # returns (text, buttons)
    text = scraper.get(f"{combot_stickers_url}{urlquote(query)}&page={page}").text
    soup = BeautifulSoup(text, "lxml")
    div = soup.find("div", class_="page__container")
    packs = div.find_all("a", class_="sticker-pack__btn")
    titles = div.find_all("div", "sticker-pack__title")
    has_prev_page = has_next_page = None
    highlighted_page = div.find("a", class_="pagination__link is-active")
    if highlighted_page is not None and user_id is not None:
        highlighted_page = highlighted_page.parent
        has_prev_page = highlighted_page.previous_sibling.previous_sibling is not None
        has_next_page = highlighted_page.next_sibling.next_sibling is not None
    buttons = []
    if has_prev_page:
        buttons.append(
            InlineKeyboardButton(text="⟨", callback_data=f"cbs_{page - 1}_{user_id}")
        )
    if has_next_page:
        buttons.append(
            InlineKeyboardButton(text="⟩", callback_data=f"cbs_{page + 1}_{user_id}")
        )
    buttons = InlineKeyboardMarkup([buttons]) if buttons else None
    text = f"sᴛɪᴄᴋᴇʀs ғᴏʀ <code>{escape(query)}</code>:\nᴘᴀɢᴇ: {page}"
    if packs and titles:
        for pack, title in zip(packs, titles):
            link = pack["href"]
            text += f"\n• <a href='{link}'>{escape(title.get_text())}</a>"
    elif page == 1:
        text = "ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ, ᴛʀʏ ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴛᴇʀᴍ"
    else:
        text += "\n\nɪɴᴛᴇʀᴇsᴛɪɴɢʟʏ, ᴛʜᴇʀᴇ's  ɴᴏᴛʜɪɴɢ ʜᴇʀᴇ."
    return text, buttons


def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ɴᴀᴍᴇ ᴛᴏ sᴇᴀʀᴄʜ ғᴏʀ ᴘᴀᴄᴋ.")
        return
    text = requests.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ :(.")
        return
    reply = f"sᴛɪᴄᴋᴇʀs ғᴏʀ *{split[1]}*:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

def cbs_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    _, page, user_id = query.data.split("_", 2)
    if int(user_id) != query.from_user.id:
        query.answer("ɴᴏᴛ ғᴏʀ ʏᴏᴜ", cache_time=60 * 60)
        return
    search_query = query.message.text.split("\n", 1)[0].split(maxsplit=2)[2][:-1]
    text, buttons = get_cbs_data(search_query, int(page), query.from_user.id)
    query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=buttons)
    query.answer()
def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        with BytesIO() as file:
            file.name = "sticker.png"
            new_file = bot.get_file(file_id)
            new_file.download(out=file)
            file.seek(0)
            bot.send_document(chat_id, document=file)
    else:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ғᴏʀ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛs PNG.",
        )

             adding_process.edit_text(
                    f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="⎋ ᴘᴀᴄᴋ ⎋", url=f"t.me/addstickers/{packname}"
                                )
                            ]
                        ]
                    )
                    adding_process.edit_text(
                        f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                        f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML,
                    )
                print(e)

        elif is_video or is_gif:
            packname = "video" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "video"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    webm_sticker=open("kangsticker.webm", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⎋ ᴘᴀᴄᴋ ⎋", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                )
                adding_process.edit_text(
                    f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        webm_sticker=open("kangsticker.webm", "rb"),
                    )
                    adding_process.delete()
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("Invalid emoji(s).")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="⎋ ᴘᴀᴄᴋ ⎋", url=f"t.me/addstickers/{packname}"
                                )
                            ]
                        ]
                    )
                    adding_process.edit_text(
                        f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                        f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML,
                    )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🙃"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            edited_keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="⎋ ᴘᴀᴄᴋ ⎋", url=f"t.me/addstickers/{packname}"
                        )
                    ]
                ]
            )
            adding_process.edit_text(
                f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                reply_markup=edited_keyboard,
                parse_mode=ParseMode.HTML,
            )
        except OSError as e:
            msg.reply_text(" sᴏʀʀʏ ɪ ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜᴀᴛ.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
                adding_process.delete()
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "png")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="⎋ ᴘᴀᴄᴋ ⎋", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                )
                adding_process.edit_text(
                    f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("Invalid emoji(s).")
            elif e.message == "Stickers_too_much":
                msg.reply_text("Max packsize reached. Press F to pay respect.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    f"<b>ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪs ➼ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            print(e)
    else:
        packs_text = "*ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ, ᴏʀ ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ!*\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs = f"t.me/addstickers/{firstpackname}"
                else:
                    packs = f"t.me/addstickers/{packname}"
        else:
            packs = f"t.me/addstickers/{packname}"

        edited_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ", url=f"{packs}"),
                ],
            ]
        )
        msg.reply_text(
            packs_text, reply_markup=edited_keyboard, parse_mode=ParseMode.MARKDOWN
        )
    try:
        if os.path.isfile("kangsticker.png"):
            os.remove("kangsticker.png")
        elif os.path.isfile("kangsticker.tgs"):
            os.remove("kangsticker.tgs")
        elif os.path.isfile("kangsticker.webm"):
            os.remove("kangsticker.webm")
        elif os.path.isfile("kang.mp4"):
            os.remove("kang.mp4")
    except:
        pass

def getvidsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.mp4")
        bot.send_video(chat_id, video=open("sticker.mp4", "rb"))
        os.remove("sticker.mp4")
    else:
        update.effective_message.reply_text(
            "Please reply to a video sticker to upload its MP4."
        )

def getvidsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.mp4")
        bot.send_video(chat_id, video=open("sticker.mp4", "rb"))
        os.remove("sticker.mp4")
    else:
        update.effective_message.reply_text(
            "Please reply to a video sticker to upload its MP4."
        )


def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text("ᴅᴇʟᴇᴛᴇᴅ!")
    else:
        update.effective_message.reply_text(
            "Please reply to sticker message to del sticker"
        )


def video(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.animation:
        file_id = msg.reply_to_message.animation.file_id
        new_file = bot.get_file(file_id)
        new_file.download("video.mp4")
        bot.send_video(chat_id, video=open("video.mp4", "rb"))
        os.remove("video.mp4")
    else:
        update.effective_message.reply_text(
            "Please reply to a gif for me to get it's video."
        )

                                            
__help__ = """
 ❍ /sᴛɪᴄᴋᴇʀɪᴅ *:* ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴛᴇʟʟ ʏᴏᴜ ɪᴛs ғɪʟᴇ ɪᴅ.
 ❍ /getsticker *:* ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛs ʀᴀᴡ ᴘɴɢ ғɪʟᴇ.
 ❍ /kang *:* ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ.
 ❍ /stickers *:* ғɪɴᴅ sᴛɪᴄᴋᴇʀs ғᴏʀ ɢɪᴠᴇɴ ᴛᴇʀᴍ ᴏɴ ᴄᴏᴍʙᴏᴛ sᴛɪᴄᴋᴇʀ ᴄᴀᴛᴀʟᴏɢᴜᴇ
"""

__mod_name__ = "Kᴀɴɢ"
STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang, admin_ok=True, run_async=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
