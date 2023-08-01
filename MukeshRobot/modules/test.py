import asyncio
from datetime import datetime, timedelta
from MukeshRobot import pbot as app
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.raw import types
import MukeshRobot.modules.no_sql.users_db as user_db 
from MukeshRobot import pbot as app
from MukeshRobot import DEV_USERS, LOGGER, OWNER_ID, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from MukeshRobot.modules.no_sql.users_db import get_all_users



def get_user_id(username):
    # ensure valid userid
    if len(username) <= 5:
        return None

    if username.startswith("@"):
        username = username[1:]

    users = user_db.get_userid_by_name(username)

    if not users:
        return None

    if len(users) == 1:
        return users[0]["_id"]

    for user_obj in users:
        try:
            userdat = dispatcher.bot.get_chat(user_obj["_id"])
            if userdat.username == username:
                return userdat.id

        except BadRequest as excp:
            if excp.message != "Chat not found":
                LOGGER.exception("Error extracting user ID")

    return None

@app.on_message(filters.command(" broadcast") & filters.user(OWNER_ID))

async def braodcast_message(client, message, _):
    
    if message.reply_to_message:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("ᴜsᴀɢᴇ**:\n/broadcast [MESSAGE] or [Reply to a Message]")
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ")

    

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await user_db.get_all_chats() 
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
            except Exception as e:
                await message.reply_text(e)
               
        try:
            await message.reply_text("ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {0} ᴜsᴇʀs".format(susr))
        except Exception as e:
            await message.reply_text(e)
            
     
