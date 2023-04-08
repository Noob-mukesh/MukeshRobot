import secureme
from pyrogram import filters
from MukeshRobot import pbot as mukesh


@mukesh.on_message(filters.command("encypt"))
async def countryinfo(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("**Example:**\n\n`/encyrpt India`")
    m = message.text.split(' ',1)[1]
    try:
        Secure = secureme.encrypt(m)
        
        await message.reply_text(Secure)
        

    except Exception as e:
        await message.reply_text(e)
