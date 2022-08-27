import asyncio
from pyrogram import filters
from MukeshRobot import pbot as app
from pyrogram.types import Message
from MukeshRobot import eor
from MukeshRobot.utils.errors import capture_err

active_channel = []


async def channel_toggle(db, message: Message):
    status = message.text.split(None, 1)[1].lower()
    chat_id = message.chat.id
    if status == "on":
        if chat_id not in db:
            db.append(chat_id)
            text = "**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ɪs 'ᴇɴᴀʙʟᴇᴅ'.ɪ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴍᴇssᴀɢᴇ ᴛʜᴀᴛ sᴇɴᴅ ᴡɪᴛʜ ᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇs🛡️**"
            return await eor(message, text=text)
        await eor(message, text="ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.")
    elif status == "off":
        if chat_id in db:
            db.remove(chat_id)
            return await eor(message, text="ᴀɴᴛɪᴄʜᴀɴɴᴇʟ ᴅɪsᴀʙʟᴇᴅ ʙᴀʙʏ🔻")
        await eor(
            message,
            text=f"**ᴀɴᴛɪ ᴄʜᴀɴɴᴇʟ ᴍᴏᴅᴇ sᴜᴄᴇssғᴜʟʟʏ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ ɪɴ ᴛʜɪs ᴄʜᴀᴛ** {message.chat.id} ❌",
        )
    else:
        await eor(
            message, text="ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ  `/antichannel on` and `/antichannel off` ᴏɴʟʏ"
        )


# Enabled | Disable antichannel


@app.on_message(filters.command("antichannel"))
@capture_err
async def antichannel_status(_, message: Message):
    if len(message.command) != 2:
        return await eor(
            message, text="ɪ ᴜɴᴅᴇʀsᴛᴀɴᴅ `/antichannel on` and `/antichannel off` ᴏɴʟʏ"
        )
    await channel_toggle(active_channel, message)


@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
        | filters.text
    )
    & ~filters.private,
    group=41,
)
async def anitchnl(_, message):
    chat_id = message.chat.id
    if message.sender_chat:
        sender = message.sender_chat.id
        if message.chat.id not in active_channel:
            return
        if chat_id == sender:
            return
        else:
            await message.delete()
            ti = await message.reply_text(
                "**A anti-channel message detected. I deleted it..!**"
            )
            await asyncio.sleep(7)
            await ti.delete()


__mod_name__ = "ᴀ-Cʜᴀɴɴᴇʟ♦️"
__help__ = """
your groups to stop anonymous channels sending messages into your chats.
**Type of messages**
        - document
        - photo
        - sticker
        - animation
        - video
        - text
        
**Admin Commands:**


 - /antichannel [on / off] - Anti- channel  function 
**Note** : If linked channel  send any containing characters in this type when on  function no del   
 🚩ᴘᴏᴡᴇʀᴇᴅ ʙʏ : [ᴍᴜᴋᴇsʜ ʙᴏᴛ ᴢᴏɴᴇ](t.me/mukeshbotzone)
 """
