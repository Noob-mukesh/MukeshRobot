import random
from datetime import datetime

from pyrogram import filters
from pyrogram.enums import ChatType

from MukeshRobot import pbot,OWNER_ID
from MukeshRobot.utils.mongo import get_couple, save_couple

# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())


@pbot.on_message(filters.command(["couple", "couples"]))
async def couple(_, message):
    if message.chat.type == "private":
        return await message.reply_text("This command only works in groups.")
    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today)
        if not is_selected:
            list_of_users = []
            if list_of_users==1726528906 and 5910057231:
  
                list_of_users.remove(5910057231,1726528906)
            list_of_users.remove(OWNER_ID)
            async for i in pbot.get_chat_members(message.chat.id):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)
            if len(list_of_users) < 2:
                return await message.reply_text("Not enough users")
            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)
            c1_mention = (await pbot.get_users(c1_id)).mention
            c2_mention = (await pbot.get_users(c2_id)).mention

            couple_selection_message = f"""** ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ 💏:**
{c1_mention} + {c2_mention} = ❤️
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await pbot.send_message(message.chat.id, text=couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today, couple)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await pbot.get_users(c1_id)).first_name
            c2_name = (await pbot.get_users(c2_id)).first_name
            couple_selection_message = f"""Couple of the day:
[{c1_name}](tg://openmessage?user_id={c1_id}) + [{c2_name}](tg://openmessage?user_id={c2_id}) = 😘
__New couple of the day may be chosen at 12AM {tomorrow}__"""
            await pbot.send_message(message.chat.id, text=couple_selection_message)
       # elif is_selected:
          #  X= int(5910057231)
           # Y = int(1726528906)
           # c1_name = (await pbot.get_users(X)).first_name
           # c2_name = (await pbot.get_users(Y)).first_name
           # couple_selection_message = f"""ᴄᴏᴜᴘʟᴇ ғᴏʀ ғᴏʀᴇᴠᴇʀ ❤:
#[{c1_name}](tg://openmessage?user_id={X}) + [{c2_name}](tg://openmessage?user_id={Y}) = 😘
#__ \n ʙᴇsᴛ ᴄᴏᴜᴘʟᴇ ᴇᴠᴇʀ ❤😍 {tomorrow}__"""
    except Exception as e:
        #print(e)
        await message.reply_text(e)


__help__ = """
ᴄʜᴏᴏsᴇ ᴄᴏᴜᴘʟᴇs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ

 ❍ /ᴄᴏᴜᴘʟᴇs *:* ᴄʜᴏᴏsᴇ 2 ᴜsᴇʀs ᴀɴᴅ sᴇɴᴅ ᴛʜᴇɪʀ ɴᴀᴍᴇ ᴀs ᴄᴏᴜᴘʟᴇs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ.
"""

__mod_name__ = "⍟ Cᴏᴜᴘʟᴇ ⍟"
