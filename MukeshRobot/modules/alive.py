import random
import asyncio
from pyrogram import filters, __version__ as pver
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telethon import __version__ as tver
from telegram import __version__ as lver
from platform import python_version as pyver
from MukeshRobot import BOT_USERNAME, OWNER_USERNAME, SUPPORT_CHAT, pbot

PHOTO = [
    "https://telegra.ph/file/4c832ec2867d2d56ec151.jpg",
    "https://telegra.ph/file/39147aab50d218ab8019b.jpg",
    "https://telegra.ph/file/c84ac64e321018a5d4aa4.jpg",
    "https://telegra.ph/file/a0a79755bc3336f47a30b.jpg",
    "https://telegra.ph/file/c6b6a247d0140e19e5d99.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="ɴᴏᴏʙ", url=f"https://t.me/itz_mst_boi"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="➕ᴀᴅᴅ ᴍᴇ ᴇʟsᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ➕",
            url=f"https://t.me/groupcontrollertgbot?startgroup=true",
        ),
    ],
]

lol = "https://telegra.ph/file/4c832ec2867d2d56ec151.jpg"


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("⚡")
    await asyncio.sleep(2)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ..")
    await asyncio.sleep(0.5)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ......")
    await asyncio.sleep(0.5)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ..")
    await asyncio.sleep(0.5)
    await accha.edit("ᴅɪɴɢ ᴅᴏɴɢ ꨄ︎ ᴀʟɪᴠɪɴɢ......")
    await accha.delete()
    await asyncio.sleep(0.5)
    umm = await m.reply_sticker(
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
    )
    await umm.delete()
    await asyncio.sleep(2)
    await m.reply_photo(
        lol,
        caption=f"""**ʜᴇʏ, ɪ ᴀᴍ 『[ᴀᴅᴠᴇɴᴛᴜʀᴇ ʀᴏʙᴏᴛ](t.me/groupcontrollertgbot)』**
   ━━━━━━━━━━━━━━━━━━━
  » **ᴍʏ ᴏᴡɴᴇʀ :** [ᴍᴜᴋᴇsʜ](https://t.me/{OWNER_USERNAME})
  
  » **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
  
  » **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
  
  » **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
  
  » **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{pyver()}`
   ━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(Mukesh),
    )
