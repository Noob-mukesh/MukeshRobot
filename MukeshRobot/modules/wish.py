import random
import asyncio
from pyrogram import filters
from MukeshRobot import pbot as MukeshRobot




wish_STRINGS = [
                     'Happy Rakshabandhan Day',
                   ]


@MukeshRobot.on_message(filters.command("wish"))
async def lel(bot, message):
    ran = random.choice(wish_STRINGS)
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.5)
    return await message.reply_text(text=ran)

__mod_name__ = "ʀᴀᴋʜɪ"

__help__ = """

ᴡɪsʜ ʟɪɴᴇ ʙᴀʙʏ
❍ /wish *:* ᴡɪsʜ ᴏɴ ғᴇsᴛɪᴠᴀʟ

 """
