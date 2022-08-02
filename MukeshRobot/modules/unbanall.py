from MukeshRobot import *
from MukeshRobot import LOGGER
from MukeshRobot.events import register
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError
from telethon.tl.types import (
    ChatBannedRights,
    )

from telethon import *
from telethon.tl import *
from telethon.errors import *

import os
from time import sleep
from telethon.errors import FloodWaitError
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

sudo = 5207640479
BOT_ID = 5559518126
CMD_HELP = '/ !'





# ================================================

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await telethn(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True



@register(pattern="^/unbanall$")
async def _(event):
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator
    if event.is_private:
      return await event.respond("__This command can be use in groups and channels!__")

    is_admin = False
    try:
      cutiepii = await telethn(GetParticipantRequest(
        event.chat_id,
        event.sender_id
      ))
    except UserNotParticipantError:
      is_admin = False
    else:
      if (
        isinstance(
          cutiepii.participant,
          (
            ChannelParticipantAdmin,
            ChannelParticipantCreator,
          )
        )
      ):
        is_admin = True
    if not is_admin:
      return await event.respond("__Only admins can Unmuteall!__")

    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Searching Participant Lists.")
    p = 0
    async for i in telethn.iter_participants(
        event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
    ):
        rights = ChatBannedRights(until_date=0, view_messages=False)
        try:
            await telethn(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"sleeping for {ex.seconds} seconds")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is banned in this chat")
        return
    required_string = "Successfully unbanned **{}** users"
    await event.reply(required_string.format(p))


@register(pattern="^/unmuteall$")
async def _(event):
    if event.is_private:
      return await event.respond("__This command can be use in groups and channels!__")

    is_admin = False
    try:
      cutiepii = await telethn(GetParticipantRequest(
        event.chat_id,
        event.sender_id
      ))
    except UserNotParticipantError:
      is_admin = False
    else:
      if (
        isinstance(
          cutiepii.participant,
          (
            ChannelParticipantAdmin,
            ChannelParticipantCreator,
          )
        )
      ):
        is_admin = True
    if not is_admin:
      return await event.respond("__Only admins can Unmuteall!__")
    chat = await event.get_chat()
    admin = chat.admin_rights.ban_users
    creator = chat.creator

    # Well
    if not admin and not creator:
        await event.reply("`I don't have enough permissions!`")
        return

    done = await event.reply("Working ...")
    p = 0
    async for i in telethn.iter_participants(
        event.chat_id, filter=ChannelParticipantsBanned, aggressive=True
    ):
        rights = ChatBannedRights(
            until_date=0,
            send_messages=False,
        )
        try:
            await telethn(functions.channels.EditBannedRequest(event.chat_id, i, rights))
        except FloodWaitError as ex:
            LOGGER.warn(f"sleeping for {ex.seconds} seconds")
            sleep(ex.seconds)
        except Exception as ex:
            await event.reply(str(ex))
        else:
            p += 1

    if p == 0:
        await done.edit("No one is muted in this chat")
        return
    required_string = "Successfully unmuted **{}** users"
    await event.reply(required_string.format(p))




@register(pattern="^/users$")
async def get_users(show):
    if not show.is_group:
        return
    if not await is_register_admin(show.input_chat, show.sender_id):
        return
    info = await telethn.get_entity(show.chat_id)
    title = info.title or "this chat"
    mentions = f"Users in {title}: \n"
    async for user in telethn.iter_participants(show.chat_id):
        mentions += (
            f"\nDeleted Account {user.id}"
            if user.deleted
            else f"\n[{user.first_name}](tg://user?id={user.id}) {user.id}"
        )

    with open("userslist.txt", "w+") as file:
        file.write(mentions)
    await telethn.send_file(
        show.chat_id,
        "userslist.txt",
        caption=f"Users in {title}",
        reply_to=show.id,
    )

    os.remove("userslist.txt")



__mod_name__ = "ᴜɴʙᴀɴᴀʟʟ"
