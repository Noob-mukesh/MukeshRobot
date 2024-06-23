from io import BytesIO
from time import sleep
from pyrogram import filters
from pyrogram.types import Message
from telegram import TelegramError, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
# import MukeshRobot.modules.no_sql.users_db as user_db 
from MukeshRobot import pbot as Mukesh
from MukeshRobot import DEV_USERS, LOGGER as  logger, OWNER_ID, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
# from MukeshRobot.modules.no_sql.users_db import get_all_users
from MukeshRobot.modules.no_sql import get_served_chats,get_served_users,remove_served_chat,remove_served_users
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    UserIsBlocked,
    PeerIdInvalid,
)
import time, asyncio, logging, datetime

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

    # for user_obj in users:
        try:
            userdat = dispatcher.bot.get_chat(user_obj["_id"])
            if userdat.username == username:
                return userdat.id

        except BadRequest as excp:
            if excp.message != "Chat not found":
                logger.exception("Error extracting user ID")

    return None



# @dev_plus
@Mukesh.on_message(filters.command(["bchat","broadcastgroups"]) & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_chats = get_served_chats() or []
    await bot.send_message(
        OWNER_ID,
        f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......",
    )
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text(f"broadcasting ..")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_chats = len(get_served_chats())

    for chat in all_chats:
        sts = await send_chat(chat["chat_id"], broadcast_msg)

        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            pass
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ ᴄʜᴀᴛꜱ  {total_chats} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_chats}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}"
            )
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ {completed_in}.\n\nTᴏᴛᴀʟ ᴄʜᴀᴛꜱ {total_chats}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_chats}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}"
    )


async def send_chat(chat_id, message):
    try:
        await message.forward(chat_id=int(chat_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(chat_id, message)
    except InputUserDeactivated:
        remove_served_chat(chat_id)
        logger.info(f"{chat_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        
        return 400
    except UserIsBlocked:
        remove_served_chat(chat_id)
        logger.info(f"{chat_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        remove_served_chat(chat_id)
        logger.info(f"{chat_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        remove_served_chat(chat_id)
        logger.error(f"{chat_id} : {e}")
        pass

# @dev_plus
# broadcast
@Mukesh.on_message(filters.command(["buser","broadcastusers"]) & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_users = get_served_users()
    await bot.send_message(
        OWNER_ID,
        f"{m.from_user.mention} or {m.from_user.id} Iꜱ ꜱᴛᴀʀᴛᴇᴅ ᴛʜᴇ Bʀᴏᴀᴅᴄᴀꜱᴛ......",
    )
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text(f"broadcasting ..")
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = len(get_served_users())
    for user in all_users:
        sts = await send_msg(user["user_id"], broadcast_msg)
        if sts == 200:
            success += 1
        else:
            failed += 1
        if sts == 400:
            pass
        done += 1
        if not done % 20:
            await sts_msg.edit(
                f"Bʀᴏᴀᴅᴄᴀꜱᴛ Iɴ Pʀᴏɢʀᴇꜱꜱ: \nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users} \nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}"
            )
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(
        f"Bʀᴏᴀᴅᴄᴀꜱᴛ Cᴏᴍᴩʟᴇᴛᴇᴅ: \nCᴏᴍᴩʟᴇᴛᴇᴅ Iɴ {completed_in}.\n\nTᴏᴛᴀʟ Uꜱᴇʀꜱ {total_users}\nCᴏᴍᴩʟᴇᴛᴇᴅ: {done} / {total_users}\nSᴜᴄᴄᴇꜱꜱ: {success}\nFᴀɪʟᴇᴅ: {failed}"
    )


async def send_msg(user_id, message):
    try:
        await message.forward(user_id)
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        remove_served_users(user_id)
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        remove_served_users(user_id)
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        remove_served_users(user_id)
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500





def __stats__():
    return f"• {len(get_served_users())} ᴜsᴇʀs, ᴀᴄʀᴏss {len(get_served_chats())} ᴄʜᴀᴛs"


def __migrate__(old_chat_id, new_chat_id):
    user_db.migrate_chat(old_chat_id, new_chat_id)


