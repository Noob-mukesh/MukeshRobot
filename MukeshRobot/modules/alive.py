import asyncio
from platform import python_version as pyver

from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver

from MukeshRobot import SUPPORT_CHAT, pbot,BOT_USERNAME, OWNER_ID

PHOTO = [
    "https://telegra.ph/file/d2a23fbe48129a7957887.jpg",
    "https://telegra.ph/file/ddf30888de58d77911ee1.jpg",
    "https://telegra.ph/file/268d66cad42dc92ec65ca.jpg",
    "https://telegra.ph/file/13a0cbbff8f429e2c59ee.jpg",
    "https://telegra.ph/file/bdfd86195221e979e6b20.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="ɴᴏᴏʙ", url=f"tg://user?id={OWNER_ID}"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="😎𝚄𝙽𝙳𝙰𝙽𝙶 𝙶𝚄𝙰 𝙽𝙶𝙰𝙱😎",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

lol = "https://telegra.ph/file/c9af9661c261fd424659f.jpg"


@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("🌠")
    await asyncio.sleep(0.5)
    await accha.edit("𝙲𝙸𝙻𝚄𝙺 𝙱𝙰𝙷 🤙 𝚆𝙰𝙷..")
    await asyncio.sleep(0.5)
    await accha.edit("𝙲𝙸𝙻𝚄𝙺 𝙱𝙰𝙷 🤙 𝚆𝙰𝙷......")
    await asyncio.sleep(0.5)
    await accha.edit("𝙲𝙸𝙻𝚄𝙺 𝙱𝙰𝙷 🤙 𝚆𝙰𝙷..")
    await asyncio.sleep(0.5)
    await accha.edit("𝙲𝙸𝙻𝚄𝙺 𝙱𝙰𝙷 🤙 𝚆𝙰𝙷......")
    await accha.delete()
    await asyncio.sleep(0.5)
    umm = await m.reply_sticker(
        ""
    )
    await umm.delete()
    await asyncio.sleep(2)
    await m.reply_photo(
        lol,
        caption=f"""**ʜᴇʏ, ɪ ᴀᴍ 『[ɢʀᴏᴜᴘ ᴄᴏɴᴛʀᴏʟʟᴇʀ](f"t.me/{BOT_USERNAME}")』**
   ━━━━━━━━━━━━━━━━━━━
  » **ᴍʏ ᴏᴡɴᴇʀ :** [𝙼𝙰𝙽𝙳𝙾𝚁](tg://user?id={OWNER_ID}))
  
  » **ʟɪʙʀᴀʀʏ ᴠᴇʀsɪᴏɴ :** `{lver}`
  
  » **ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{tver}`
  
  » **ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ :** `{pver}`
  
  » **ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ :** `{pyver()}`
   ━━━━━━━━━━━━━━━━━━━""",
        reply_markup=InlineKeyboardMarkup(Mukesh),
    )
