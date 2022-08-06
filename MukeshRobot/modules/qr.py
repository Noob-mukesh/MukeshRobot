import os
from MukeshRobot import telethn
from asyncio import sleep
from datetime import datetime
from telegram.ext import CommandHandler
from requests import get
from requests import post
from telethon import types
from telethon.tl import functions
from MukeshRobot.events import register
from MukeshRobot import MONGO_DB_URI
from pymongo import MongoClient


client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["Amanda"]
approved_users = db.approve


def progress(current, total):
    """ Calculate and return the download progress with given arguments. """
    print(
        "Downloaded {} of {}\nCompleted {}".format(
            current, total, (current / total) * 100
        )
    )


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await pbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await pbot.get_peer_id(user)
        ps = (
            await pbot(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None


@register(pattern=r"^/getqr$")
async def parseqr(qr_e):
    """ For .getqr command, get QR Code content from the replied photo. """
    if qr_e.fwd_from:
        return

    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]

    if qr_e.is_group:
        if (await is_register_admin(qr_e.input_chat, qr_e.message.sender_id)):
            pass
        elif qr_e.chat_id == iid and qr_e.sender_id == userss:
            pass
        else:
            return

    start = datetime.now()
    downloaded_file_name = await pbot.download_media(
        await qr_e.get_reply_message(), progress_callback=progress
    )
    url = "https://api.qrserver.com/v1/read-qr-code/?outputformat=json"
    file = open(downloaded_file_name, "rb")
    files = {"file": file}
    resp = post(url, files=files).json()
    qr_contents = resp[0]["symbol"][0]["data"]
    file.close()
    os.remove(downloaded_file_name)
    end = datetime.now()
    duration = (end - start).seconds
    await qr_e.reply(
        "Obtained QRCode contents in {} seconds.\n{}".format(duration, qr_contents)
    )


@register(pattern=r"^/makeqr(?: |$)([\s\S]*)")
async def makeqr(qrcode):
    """ For .makeqr command, make a QR Code containing the given content. """
    if qrcode.fwd_from:
        return
    approved_userss = approved_users.find({})
    for ch in approved_userss:
        iid = ch["id"]
        userss = ch["user"]

    if qrcode.is_group:
        if (await is_register_admin(qrcode.input_chat, qrcode.message.sender_id)):
            pass
        elif qrcode.chat_id == iid and qrcode.sender_id == userss:
            pass
        else:
            return

    start = datetime.now()
    input_str = qrcode.pattern_match.group(1)
    message = "SYNTAX: `/makeqr <long text to include>`"
    reply_msg_id = None
    if input_str:
        message = input_str
    elif qrcode.reply_to_msg_id:
        previous_message = await qrcode.get_reply_message()
        reply_msg_id = previous_message.id
        if previous_message.media:
            downloaded_file_name = await pbot.download_media(
                previous_message, progress_callback=progress
            )
            m_list = None
            with open(downloaded_file_name, "rb") as file:
                m_list = file.readlines()
            message = ""
            for media in m_list:
                message += media.decode("UTF-8") + "\r\n"
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message

    url = "https://api.qrserver.com/v1/create-qr-code/?data={}&\
size=200x200&charset-source=UTF-8&charset-target=UTF-8\
&ecc=L&color=0-0-0&bgcolor=255-255-255\
&margin=1&qzone=0&format=jpg"

    resp = get(url.format(message), stream=True)
    required_file_name = "temp_qr.webp"
    with open(required_file_name, "w+b") as file:
        for chunk in resp.iter_content(chunk_size=128):
            file.write(chunk)
    await pbot.send_file(
        qrcode.chat_id,
        required_file_name,
        reply_to=reply_msg_id,
        progress_callback=progress,
    )
    os.remove(required_file_name)
    duration = (datetime.now() - start).seconds
    await qrcode.reply("Created QRCode in {} seconds".format(duration))

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")

__help__ = """
 - /getqr: get the qr code content from the replied qr code
 - /makeqr <content>: make a qr code from the given message (text, link, etc...)
"""

__mod_name__ = "GᴇɴQʀ"

GETQR_HANDLER = CommandHandler("getqr", parseqr)
MAKEQR_HANDLER = CommandHandler("makeqr", makeqr)

dispatcher.add_handler(GETQR_HANDLER)
dispatcher.add_handler(MAKEQR_HANDLER)

__command_list__ = ["getqr"]
__command_list__ = ["makeqr"]
__handlers__ = [GETQR_HANDLER]
__handlers__ = [MAKEQR_HANDLER]
