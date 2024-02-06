import requests
from MukeshRobot import pbot as mukesh
from pyrogram import filters

@mukesh.on_message(filters.command("hastag"))
async def hastag(bot, message):
    
    try:
        text = message.text.split(' ',1)[1]
        res = requests.get(f"https://mukesh-api.vercel.app/hastag?query={text}").json()["results"]

    except IndexError:
        return await message.reply_text("Example:\n\n`/hastag python`")
        
    
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{res}</pre>", quote=True)
    
__mod_name__ = "Hᴀsʜᴛᴀɢ"
__help__= """
**Yᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ʜᴀsʜᴛᴀɢ ɢᴇɴᴇʀᴀᴛᴏʀ ᴡʜɪᴄʜ ᴡɪʟʟ ɢɪᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴛᴏᴘ 𝟹𝟶 ᴀɴᴅ ᴍᴏʀᴇ ʜᴀsʜᴛᴀɢs ʙᴀsᴇᴅ ᴏғғ ᴏғ ᴏɴᴇ ᴋᴇʏᴡᴏʀᴅ sᴇʟᴇᴄᴛɪᴏɴ.**
° /hastag enter word to generate hastag.
°Exᴀᴍᴘʟᴇ: ` /hastag python `"""

