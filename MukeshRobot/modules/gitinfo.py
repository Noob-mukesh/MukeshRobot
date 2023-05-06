from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MukeshRobot import pbot
from MukeshRobot.utils.errors import capture_err


@pbot.on_message(filters.command("github"))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        return await message.reply_text("/git Noob-Mukesh")
    username = message.text.split(None, 1)[1]
    URL = f"https://api.github.com/users/{username}"
    async with ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")
            result = await request.json()
            try:
                url = result["html_url"]
                name = result["name"]
                company = result["company"]
                bio = result["bio"]
                created_at = result["created_at"]
                avatar_url = result["avatar_url"]
                blog = result["blog"]
                location = result["location"]
                repositories = result["public_repos"]
                followers = result["followers"]
                following = result["following"]
                caption = f"""**Info Of {name}**
**ᴜsᴇʀɴᴀᴍᴇ :** `{username}`
**ʙɪᴏ :** `{bio}`
**ᴄᴏᴍᴘᴀɴʏ :** `{company}`
**ᴄʀᴇᴀᴛᴇᴅ ᴏɴ:** `{created_at}`
**ʀᴇᴘᴏsɪᴛᴏʀɪᴇs :** `{repositories}`
**ʙʟᴏɢ :** `{blog}`
**ʟᴏᴄᴀᴛɪᴏɴ :** `{location}`
**ғᴏʟʟᴏᴡᴇʀs  :** `{followers}`
**ғᴏʟʟᴏᴡɪɴɢ :** `{following}`"""
            except:
                print(str(e))
     Mukesh = 
    [[
        InlineKeyboardButton(text="ᴘʀᴏғɪʟᴇ ʟɪɴᴋ", url=url),
        InlineKeyboardButton("Cʟᴏsᴇ",callback_data="close_reply)
       
    ]]           
    await message.reply_photo(photo=avatar_url, caption=caption,reply_markup=InlineKeyboardMarkup(Mukesh))


__mod_name__ = "⍟ Gɪᴛʜᴜʙ ⍟"

__help__ = """
ɪ ᴡɪʟʟ ɢɪᴠᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ɢɪᴛʜᴜʙ ᴘʀᴏғɪʟᴇ 

 ❍ /github <ᴜsᴇʀɴᴀᴍᴇ>*:* ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴀ ɢɪᴛʜᴜʙ ᴜsᴇʀ.
"""
