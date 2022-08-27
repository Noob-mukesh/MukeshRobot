from pyrogram import filters

from MukeshRobot import pbot, arq, BOT_USERNAME


@pbot.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        return await message.reply_text(data.result)
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    statistics = f"""
**>-< sʏsᴛᴇᴍ >-<**
**ᴜᴘᴛɪᴍᴇ:** `{uptime}`
**ʀᴇǫᴜᴇsᴛs sɪɴᴄᴇ ᴜᴘᴛɪᴍᴇ:** `{requests}`
**ᴄᴘᴜ:** `{cpu}`
**ᴍᴇᴍᴏʀʏ:**
**ᴛᴏᴛᴀʟ sᴇʀᴠᴇ:** `{server_mem}`
**ᴀᴘɪ:** `{api_mem}`
**ᴅɪsᴋ:** `{disk}`
**ᴘʟᴀᴛғᴏʀᴍ:** `{platform}`
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** `{python_version}`

**ᴀʀǫ sᴛᴀᴛɪsᴛɪᴄs:**
**ᴜsᴇʀs:** `{users}`

**@{BOT_USERNAME} sᴏᴍᴇ ᴍᴏᴅᴜʟᴇs ʀᴜɴɴɪɴɢ ᴀʀǫ**
"""
    await message.reply_text(statistics, disable_web_page_preview=True)


__mod_name__ = "ᴀʀǫ📍"
__help__ = f""" /arq ᴛᴏ ᴄʜᴇᴀᴋ ᴀʀǫ ʟᴇᴠᴇʟ ᴏғ ᴛʜᴇ ʙᴏᴛ"""
