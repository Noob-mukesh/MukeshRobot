import secureme
from MukeshRobot import pbot as mukesh
from pyrogram import filters
@mukesh.on_message(filters.command("encrypt"))
async def secure(bot, message):
     if len(message.command) < 2:
           return await message.reply_text("Example:\n\n/encrypt Mukesh ")
    m = message.text.split(' ')[1]
    try:
        k = secureme.encrypt(m)
        await message.reply_text(k)
    except Exception as e:
        await message.reply_text(f"Error {e}")
