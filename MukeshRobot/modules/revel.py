from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import Message
from MukeshRobot import (
    BOT_NAME,
    BOT_USERNAME,
    LOGGER,
    OWNER_ID,
    START_IMG,
    SUPPORT_CHAT,
    TOKEN,
    StartTime,
    dispatcher,
    pbot,
    telethn,
    updater)
# from MukeshRobot.config import Development as Config
# API_ID = Config.API_ID
# API_HASH = Config.API_HASH
# ALLOW_CHATS = Config.ALLOW_CHATS
# ALLOW_EXCL = Config.ALLOW_EXCL
# CASH_API_KEY = Config.CASH_API_KEY
# DB_URI = Config.DATABASE_URL
# DEL_CMDS = Config.DEL_CMDS
# EVENT_LOGS = Config.EVENT_LOGS
# INFOPIC = Config.INFOPIC
# LOAD = Config.LOAD
# MONGO_DB_URI = Config.MONGO_DB_URI
# NO_LOAD = Config.NO_LOAD
# START_IMG = Config.START_IMG
# STRICT_GBAN = Config.STRICT_GBAN
# SUPPORT_CHAT = Config.SUPPORT_CHAT
# TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
# TOKEN = Config.TOKEN
# TIME_API_KEY = Config.TIME_API_KEY
# WORKERS = Config.WORKERS

# try:
#     OWNER_ID = int(Config.OWNER_ID)
# except ValueError:
#     raise Exception("Your OWNER_ID variable is not a valid integer.")

# try:
#     BL_CHATS = set(int(x) for x in Config.BL_CHATS or [])
# except ValueError:
#     raise Exception("Your blacklisted chats list does not contain valid integers.")

# try:
#     DRAGONS = set(int(x) for x in Config.DRAGONS or [])
#     DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
# except ValueError:
#     raise Exception("Your sudo or dev users list does not contain valid integers.")

# try:
#     DEMONS = set(int(x) for x in Config.DEMONS or [])
# except ValueError:
#     raise Exception("Your support users list does not contain valid integers.")

# try:
#     TIGERS = set(int(x) for x in Config.TIGERS or [])
# except ValueError:
#     raise Exception("Your tiger users list does not contain valid integers.")

# try:
#     WOLVES = set(int(x) for x in Config.WOLVES or [])
# except ValueError:
#     raise Exception("Your whitelisted users list does not contain valid integers.")



# DRAGONS.add(OWNER_ID)
# DEV_USERS.add(OWNER_ID)

from MukeshRobot import BOT_NAME
from MukeshRobot import pbot as app

@app.on_message(
    filters.command(["con", "var"]) & filters.user(OWNER_ID)
)
async def get_vars(_, message: Message):
    try:
        await app.send_message(
            chat_id=int(OWNER_ID),
            text=f"""<u>**{BOT_NAME} ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs :**</u>

**ʙᴏᴛ_ᴛᴏᴋᴇɴ :** `{TOKEN}`




""")
    except:
        return await message.reply_text("» ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs.")
    if message.chat.type != ChatType.PRIVATE:
        await message.reply_text(
            "» ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴘᴍ, ɪ'ᴠᴇ sᴇɴᴛ ᴛʜᴇ ᴄᴏɴғɪɢ ᴠᴀʀɪᴀʙʟᴇs ᴛʜᴇʀᴇ."
        )
