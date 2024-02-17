from io import BytesIO
from time import sleep
from pyrogram import filters
from pyrogram.types import Message
from telegram import TelegramError, Update
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
import MukeshRobot.modules.no_sql.users_db as user_db 
from MukeshRobot import pbot as Mukesh
from MukeshRobot import DEV_USERS, LOGGER as  logger, OWNER_ID, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import dev_plus, sudo_plus
from MukeshRobot.modules.no_sql.users_db import get_all_users
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

    for user_obj in users:
        try:
            userdat = dispatcher.bot.get_chat(user_obj["_id"])
            if userdat.username == username:
                return userdat.id

        except BadRequest as excp:
            if excp.message != "Chat not found":
                logger.exception("Error extracting user ID")

    return None



@dev_plus
@Mukesh.on_message(filters.command(["bchat","broadcastgroups"]) & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_chats = user_db.get_all_chats() or []
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
    total_chats = len(user_db.get_all_chats())

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
        logger.info(f"{chat_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{chat_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{chat_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{chat_id} : {e}")
        pass

@dev_plus
# broadcast
@Mukesh.on_message(filters.command(["buser","broadcastusers"]) & filters.user(OWNER_ID) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_users = get_all_users()
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
    total_users = len(get_all_users())
    for user in all_users:
        sts = await send_msg(user["_id"], broadcast_msg)
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
        await message.forward(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : Bʟᴏᴄᴋᴇᴅ Tʜᴇ Bᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : Uꜱᴇʀ Iᴅ Iɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500




def log_user(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message

    user_db.update_user(msg.from_user.id, msg.from_user.username, chat.id, chat.title)

    if msg.reply_to_message:
        user_db.update_user(
            msg.reply_to_message.from_user.id,
            msg.reply_to_message.from_user.username,
            chat.id,
            chat.title,
        )

    if msg.forward_from:
        user_db.update_user(msg.forward_from.id, msg.forward_from.username)


@sudo_plus
def chats(update: Update, context: CallbackContext):
    all_chats = user_db.get_all_chats() or []
    chatfile = "List of chats.\n0. Chat Name  Chat ID | Chat Member"
    P = 1
    for chat in all_chats:
        try:
            chat_id=chat["chat_id"]
            curr_chat = context.bot.getChat(chat.chat_id)
            curr_chat.get_member(context.bot.id)
            chat_members = curr_chat.get_member_count(context.bot.id)
            chatfile += f"{P} {chat.chat_name} | {chat_id} | {chat_members}"
            P = P + 1
        except:
            pass

    with BytesIO(str.encode(chatfile)) as output:
        output.name = "groups_list.txt"
        update.effective_message.reply_document(
            document=output,
            filename="groups_list.txt",
            caption="Here be the list of groups in my database.",
        )


def chat_checker(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if update.effective_message.chat.get_member(bot.id).can_send_messages is False:
            bot.leaveChat(update.effective_message.chat.id)
    except Unauthorized:
        pass


def __user_info__(user_id):
    if user_id in [777000, 1087968824]:
        return """<b>➻ ᴄᴏᴍᴍᴏɴ ᴄʜᴀᴛs:</b> <code>???</code>"""
    if user_id == dispatcher.bot.id:
        return """<b>➻ ᴄᴏᴍᴍᴏɴ ᴄʜᴀᴛs:</b> <code>???</code>"""
    num_chats = user_db.get_user_num_chats(user_id)
    return f"""<b>➻ ᴄᴏᴍᴍᴏɴ ᴄʜᴀᴛs:</b> <code>{num_chats}</code>"""


def __stats__():
    return f"• {user_db.num_users()} ᴜsᴇʀs, ᴀᴄʀᴏss {user_db.num_chats()} ᴄʜᴀᴛs"


def __migrate__(old_chat_id, new_chat_id):
    user_db.migrate_chat(old_chat_id, new_chat_id)


__help__ = ""  # no help string

# BROADCAST_HANDLER = CommandHandler(
#     ["broadcastall", "broadcastusers", "broadcastgroups"], broadcast, run_async=True
# )
USER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, log_user, run_async=True
)
CHAT_CHECKER_HANDLER = MessageHandler(
    Filters.all & Filters.chat_type.groups, chat_checker, run_async=True
)
CHATLIST_HANDLER = CommandHandler("groups", chats, run_async=True)

dispatcher.add_handler(USER_HANDLER, USERS_GROUP)
# dispatcher.add_handler(BROADCAST_HANDLER)
dispatcher.add_handler(CHATLIST_HANDLER)
dispatcher.add_handler(CHAT_CHECKER_HANDLER, CHAT_GROUP)

__mod_name__ = "Usᴇʀs"
__handlers__ = [(USER_HANDLER, USERS_GROUP), CHATLIST_HANDLER]
