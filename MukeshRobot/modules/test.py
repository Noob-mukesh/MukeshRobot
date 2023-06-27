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

USERS_GROUP = 4
CHAT_GROUP = 5
DEV_AND_MORE = DEV_USERS.append(int(OWNER_ID))


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

AUTO_SLEEP = 5
IS_BROADCASTING = False
cleanmode_group = 15



@app.on_message(filters.command(" broadcast") & filters.user(OWNER_ID))

async def braodcast_message(client, message, _):
    global IS_BROADCASTING
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

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await user_db.get_all_chats() or []
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if i == -1001686672798:
                continue
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent, pin))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_all_users()
        for user in susers:
            served_users.append(int(user["_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text("ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {0} ᴜsᴇʀs".format(susr))
        except:
            pass
    IS_BROADCASTING = False    
