import html
import re
from typing import Optional

from telegram import Chat, ChatPermissions, Message, Update, User
from telegram.error import BadRequest
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

from MukeshRobot import TIGERS, WOLVES, dispatcher
from MukeshRobot.modules.connection import connected
from MukeshRobot.modules.helper_funcs.alternate import send_message
from MukeshRobot.modules.helper_funcs.chat_status import (
    bot_admin,
    is_user_admin,
    user_admin,
    user_admin_no_reply,
)
from MukeshRobot.modules.helper_funcs.string_handling import extract_time
from MukeshRobot.modules.log_channel import loggable
from MukeshRobot.modules.sql import antiflood_sql as sql
from MukeshRobot.modules.sql.approve_sql import is_approved

FLOOD_GROUP = 3


@loggable
def check_flood(update, context) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]
    if not user:  # ignore channels
        return ""

    # ignore admins and whitelists
    if is_user_admin(chat, user.id) or user.id in WOLVES or user.id in TIGERS:
        sql.update_flood(chat.id, None)
        return ""
    # ignore approved users
    if is_approved(chat.id, user.id):
        sql.update_flood(chat.id, None)
        return
    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        getmode, getvalue = sql.get_flood_setting(chat.id)
        if getmode == 1:
            chat.ban_member(user.id)
            execstrings = "Banned"
            tag = "BANNED"
        elif getmode == 2:
            chat.ban_member(user.id)
            chat.unban_member(user.id)
            execstrings = "Kicked"
            tag = "KICKED"
        elif getmode == 3:
            context.bot.restrict_chat_member(
                chat.id, user.id, permissions=ChatPermissions(can_send_messages=False)
            )
            execstrings = "Muted"
            tag = "MUTED"
        elif getmode == 4:
            bantime = extract_time(msg, getvalue)
            chat.kick_member(user.id, until_date=bantime)
            execstrings = "ʙᴀɴɴᴇᴅ ғᴏʀ {}".format(getvalue)
            tag = "TBAN"
        elif getmode == 5:
            mutetime = extract_time(msg, getvalue)
            context.bot.restrict_chat_member(
                chat.id,
                user.id,
                until_date=mutetime,
                permissions=ChatPermissions(can_send_messages=False),
            )
            execstrings = "ᴍᴜᴛᴇᴅ ғᴏʀ ☞︎︎︎ {}".format(getvalue)
            tag = "TMUTE"
        send_message(
            update.effective_message, "Beep Boop! Boop Beep!\n{}!".format(execstrings)
        )

        return (
            "<b>{}:</b>"
            "\n#{}"
            "\n<b>User:</b> {}"
            "\nғʟᴏᴏᴅᴇᴅ ᴛʜᴇ ɢʀᴏᴜᴘ ɴᴏᴏʙ.".format(
                tag,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )

    except BadRequest:
        msg.reply_text(
            "I ᴄᴀɴ'ᴛ ʀᴇsᴛʀɪᴄᴛ 🚫 ᴘᴇᴏᴘʟᴇ ʜᴇʀᴇ, ɢɪᴠᴇ ᴍᴇ ᴘᴇʀᴍɪssɪᴏɴs ғɪʀsᴛ ᴜɴᴛɪʟ, ɪ'ʟʟ ᴅɪsᴀʙʟᴇ ᴀɴᴛɪғʟᴏᴏᴅ ʟᴏʟ ᴏᴡɴᴇʀ."
        )
        sql.set_flood(chat.id, 0)
        return (
            "<b>{}:</b>"
            "\n#INFO"
            "\nᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs sᴏ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅɪsᴀʙʟᴇᴅ ᴀɴᴛɪ-ғʟᴏᴏᴅ".format(
                chat.title
            )
        )


@user_admin_no_reply
@bot_admin
def flood_button(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"unmute_flooder\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat = update.effective_chat.id
        try:
            bot.restrict_chat_member(
                chat,
                int(user_id),
                permissions=ChatPermissions(
                    can_send_messages=True,
                    can_send_media_messages=True,
                    can_send_other_messages=True,
                    can_add_web_page_previews=True,
                ),
            )
            update.effective_message.edit_text(
                f"ᴜɴᴍᴜᴛᴇᴅ ʙʏ ♥︎{mention_html(user.id, html.escape(user.first_name))}.",
                parse_mode="HTML",
            )
        except:
            pass


@user_admin
@loggable
def set_flood(update, context) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "This command is meant to use in group not in PM",
            )
            return ""
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if len(args) >= 1:
        val = args[0].lower()
        if val in ["off", "no", "0"]:
            sql.set_flood(chat_id, 0)
            if conn:
                text = message.reply_text(
                    "Antiflood has been disabled in {}.".format(chat_name)
                )
            else:
                text = message.reply_text("Antiflood has been disabled.")

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat_id, 0)
                if conn:
                    text = message.reply_text(
                        "Antiflood has been disabled in {}.".format(chat_name)
                    )
                else:
                    text = message.reply_text("Antiflood has been disabled.")
                return (
                    "<b>{}:</b>"
                    "\n#SETFLOOD"
                    "\n<b>Admin:</b> {}"
                    "\nDisable antiflood.".format(
                        html.escape(chat_name),
                        mention_html(user.id, html.escape(user.first_name)),
                    )
                )

            elif amount <= 3:
                send_message(
                    update.effective_message,
                    "Antiflood must be either 0 (disabled) or number greater than 3!",
                )
                return ""

            else:
                sql.set_flood(chat_id, amount)
                if conn:
                    text = message.reply_text(
                        "Anti-flood has been set to {} in chat: {}".format(
                            amount, chat_name
                        )
                    )
                else:
                    text = message.reply_text(
                        "Successfully updated anti-flood limit to {}!".format(amount)
                    )
                return (
                    "<b>{}:</b>"
                    "\n#SETFLOOD"
                    "\n<b>Admin:</b> {}"
                    "\nsᴇᴛ ᴀɴᴛɪғʟᴏᴏᴅ ᴛᴏ <code>{}</code>.".format(
                        html.escape(chat_name),
                        mention_html(user.id, html.escape(user.first_name)),
                        amount,
                    )
                )

        else:
            message.reply_text("ɪɴᴠᴀʟɪᴅ ᴀʀɢᴜᴍᴇɴᴛ ᴘʟᴇᴀsᴇ ᴜsᴇ ᴀ ɴᴜᴍʙᴇʀ, 'off' or 'no'")
    else:
        message.reply_text(
            (
                "Usᴇ `/setflood number` ᴛᴏ ᴇɴᴀʙʟᴇ ᴀɴᴛɪ-ғʟᴏᴏᴅ.\nᴏʀ ᴜsᴇ `/setflood off` ᴛᴏ ᴅɪsᴀʙʟᴇ ᴀɴᴛɪғʟᴏᴏᴅ!."
            ),
            parse_mode="markdown",
        )
    return ""


def flood(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message

    conn = connected(context.bot, update, chat, user.id, need_admin=False)
    if conn:
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴍᴇᴀɴᴛ ᴛᴏ ᴜsᴇ  ɪɴ ɢʀᴏᴜᴘ ɴᴏᴛ ɪɴ ᴍʏ ᴘᴍ ɴᴏᴏʙ",
            )
            return
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        if conn:
            text = msg.reply_text(
                "I'ᴍ ɴᴏᴛ ғᴏʀᴄɪɴɢ ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ɪɴ  {}!".format(chat_name)
            )
        else:
            text = msg.reply_text("ɪ'ᴍ ɴᴏᴛ ᴇɴғᴏʀᴄɪɴɢ  ᴀɴʏ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ ʜᴇʀᴇ!")
    else:
        if conn:
            text = msg.reply_text(
                "ɪ'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀs ᴀғᴛᴇʀ {} ᴄᴏɴsᴇᴄᴛɪᴠᴇ ᴍᴇssᴀɢᴇs. {}.".format(
                    limit, chat_name
                )
            )
        else:
            text = msg.reply_text(
                "I'ᴍ ᴄᴜʀʀᴇɴᴛʟʏ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴍᴇᴍʙᴇʀ ᴀғᴛᴇʀ {} ᴄᴏɴsᴇᴄᴜᴛɪᴠᴇ ᴍᴇssᴀɢᴇs.".format(
                    limit
                )
            )


@user_admin
def set_flood_mode(update, context):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]
    args = context.args

    conn = connected(context.bot, update, chat, user.id, need_admin=True)
    if conn:
        chat = dispatcher.bot.getChat(conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat(conn).title
    else:
        if update.effective_message.chat.type == "private":
            send_message(
                update.effective_message,
                "This command is meant to use in group not in PM",
            )
            return ""
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args[0].lower() == "ban":
            settypeflood = "ban"
            sql.set_flood_strength(chat_id, 1, "0")
        elif args[0].lower() == "kick":
            settypeflood = "kick"
            sql.set_flood_strength(chat_id, 2, "0")
        elif args[0].lower() == "mute":
            settypeflood = "mute"
            sql.set_flood_strength(chat_id, 3, "0")
        elif args[0].lower() == "tban":
            if len(args) == 1:
                teks = """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tban <timevalue>`.
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks."""
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "tban for {}".format(args[1])
            sql.set_flood_strength(chat_id, 4, str(args[1]))
        elif args[0].lower() == "tmute":
            if len(args) == 1:
                teks = (
                    update.effective_message,
                    """It looks like you tried to set time value for antiflood but you didn't specified time; Try, `/setfloodmode tmute <timevalue>`.
Examples of time value: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks.""",
                )
                send_message(update.effective_message, teks, parse_mode="markdown")
                return
            settypeflood = "tmute for {}".format(args[1])
            sql.set_flood_strength(chat_id, 5, str(args[1]))
        else:
            send_message(
                update.effective_message, "I only understand ban/kick/mute/tban/tmute!"
            )
            return
        if conn:
            text = msg.reply_text(
                "Exceeding consecutive flood limit will result in {} in {}!".format(
                    settypeflood, chat_name
                )
            )
        else:
            text = msg.reply_text(
                "Exceeding consecutive flood limit will result in {}!".format(
                    settypeflood
                )
            )
        return (
            "<b>{}:</b>\n"
            "<b>Admin:</b> {}\n"
            "Has changed antiflood mode. User will {}.".format(
                settypeflood,
                html.escape(chat.title),
                mention_html(user.id, html.escape(user.first_name)),
            )
        )
    else:
        getmode, getvalue = sql.get_flood_setting(chat.id)
        if getmode == 1:
            settypeflood = "ban"
        elif getmode == 2:
            settypeflood = "kick"
        elif getmode == 3:
            settypeflood = "mute"
        elif getmode == 4:
            settypeflood = "tban for {}".format(getvalue)
        elif getmode == 5:
            settypeflood = "tmute for {}".format(getvalue)
        if conn:
            text = msg.reply_text(
                "Sending more messages than flood limit will result in {} in {}.".format(
                    settypeflood, chat_name
                )
            )
        else:
            text = msg.reply_text(
                "Sending more message than flood limit will result in {}.".format(
                    settypeflood
                )
            )
    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "Not enforcing to flood control."
    else:
        return "Antiflood has been set to`{}`.".format(limit)


__help__ = """
*ᴀɴᴛɪғʟᴏᴏᴅ* ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴏɴ ᴜsᴇʀs ᴛʜᴀᴛ sᴇɴᴅ ᴍᴏʀᴇ ᴛʜᴀɴ x ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʀᴏᴡ. ᴇxᴄᴇᴇᴅɪɴɢ ᴛʜᴇ sᴇᴛ ғʟᴏᴏᴅ \
ᴡɪʟʟ ʀᴇsᴜʟᴛ ɪɴ ʀᴇsᴛʀɪᴄᴛɪɴɢ ᴛʜᴀᴛ ᴜsᴇʀ.
 ᴛʜɪs ᴡɪʟʟ ᴍᴜᴛᴇ ᴜsᴇʀs ɪғ ᴛʜᴇʏ sᴇɴᴅ ᴍᴏʀᴇ ᴛʜᴀɴ 10 ᴍᴇssᴀɢᴇs ɪɴ ᴀ ʀᴏᴡ, ʙᴏᴛs ᴀʀᴇ ɪɢɴᴏʀᴇᴅ.

 ❍ /flood *:* ɢᴇᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ sᴇᴛᴛɪɴɢ
• *ᴀᴅᴍɪɴs ᴏɴʟʏ:*
 ❍ /setflood <ɪɴᴛ/'ɴᴏ'/'ᴏғғ'>*:* ᴇɴᴀʙʟᴇs ᴏʀ ᴅɪsᴀʙʟᴇs ғʟᴏᴏᴅ ᴄᴏɴᴛʀᴏʟ
 *ᴇxᴀᴍᴘʟᴇ:* `/sᴇᴛғʟᴏᴏᴅ 10`
 ❍ /setfloodmode <ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛʙᴀɴ/ᴛᴍᴜᴛᴇ> <ᴠᴀʟᴜᴇ>*:* ᴀᴄᴛɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴡʜᴇɴ ᴜsᴇʀ ʜᴀᴠᴇ ᴇxᴄᴇᴇᴅᴇᴅ ғʟᴏᴏᴅ ʟɪᴍɪᴛ. ʙᴀɴ/ᴋɪᴄᴋ/ᴍᴜᴛᴇ/ᴛᴍᴜᴛᴇ/ᴛʙᴀɴ
• *ɴᴏᴛᴇ:*
 • ᴠᴀʟᴜᴇ ᴍᴜsᴛ ʙᴇ ғɪʟʟᴇᴅ ғᴏʀ ᴛʙᴀɴ ᴀɴᴅ ᴛᴍᴜᴛᴇ!!
 ɪᴛ ᴄᴀɴ ʙᴇ:
 `5ᴍ` = 5 ᴍɪɴᴜᴛᴇs
 `6ʜ` = 6 ʜᴏᴜʀs
 `3ᴅ` = 3 ᴅᴀʏs
 `1ᴡ` = 1 ᴡᴇᴇᴋ
 """

__mod_name__ = "Fʟᴏᴏᴅ"

FLOOD_BAN_HANDLER = MessageHandler(
    Filters.all & ~Filters.status_update & Filters.chat_type.groups,
    check_flood,
    run_async=True,
)
SET_FLOOD_HANDLER = CommandHandler(
    "setflood", set_flood, filters=Filters.chat_type.groups, run_async=True
)

SET_FLOOD_MODE_HANDLER = CommandHandler(
    "setfloodmode", set_flood_mode, pass_args=True, run_async=True
)  # , filters=Filters.chat_type.groups)
FLOOD_QUERY_HANDLER = CallbackQueryHandler(
    flood_button, pattern=r"unmute_flooder", run_async=True
)
FLOOD_HANDLER = CommandHandler(
    "flood", flood, filters=Filters.chat_type.groups, run_async=True
)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(FLOOD_QUERY_HANDLER)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(SET_FLOOD_MODE_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)

__handlers__ = [
    (FLOOD_BAN_HANDLER, FLOOD_GROUP),
    SET_FLOOD_HANDLER,
    FLOOD_HANDLER,
    SET_FLOOD_MODE_HANDLER,
]
