# -----------CREDITS -----------
# telegram : @legend_coder
# github : noob-mukesh
from pyrogram import filters
from .. import pbot as Mukesh,OWNER_ID
from pyrogram.types import ChatPrivileges,ChatPermissions
from pyrogram.types import *
from MukeshRobot.modules.no_sql import add_gban,remove_gban,is_gban,get_served_chats,get_gban_list,is_user_ingbanned
@Mukesh.on_message(filters.command("gban") & filters.user(OWNER_ID) & ( filters.group | filters.channel) )
async def  banuser(b,message):
    reason=""
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
        r=message.text.split()[1:] if message.reply_to_message else None
        reason+=r
        u=is_user_ingbanned(user)
        if u:
            return await message.reply_text("User is already gbanned")
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1].split()[0]
        r= " ".join(message.command[2:]) if len(message.command) > 2 else None
        print(r)
        reason+=r
    success=0
    hm = await Mukesh.get_users(user)
    try:
        all_chats =get_served_chats()
        for chat in all_chats:
            
            try:
                sts=await b.ban_chat_member(chat["chat_id"],user)
                add_gban(user_id=user,gban_reason=reason)
                success += 1
            except Exception as e:
                print(e)
        await message.reply_text(f"gbanned from {success} chats \n user :> {hm.mention()} reason {reason}")
    except Exception as e:
        await message.reply_text(f"failed due to {e}")
@Mukesh.on_message(filters.command("ungban") & filters.user(OWNER_ID) & ( filters.group | filters.channel) )
async def  unbanuser(b,message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
        u=is_user_ingbanned(user)
        if not u:
            return await message.reply_text("User is not gbanned yet")
    elif not message.reply_to_message and len(message.command) != 1:
        user = message.text.split(None, 1)[1]
       
    success=0
    hm = await Mukesh.get_users(user)
    try:
        all_chats =get_served_chats()
        for chat in all_chats:
            
            try:
                sts=await b.unban_chat_member(chat["chat_id"],user)
                remove_gban(user_id=user)
                success += 1
            except Exception as e:
                print(e)
        await message.reply_text(f"ungbanned from {success} chats \n user :> {hm.mention()}")
    except Exception as e:
        await message.reply_text(f"failed due to {e}")
@Mukesh.on_message(filters.command("gbanlist") & filters.user(OWNER_ID))
async def get_gban_listss(_,m)  :
    banned=get_gban_list()
    if len(get_gban_list())==0:
        return await m.reply_text("No users are gbanned")
    text="Gbanned Users:\n"
    for user in banned :
        text+=f"• {user['user_id']} - {user['gban_reason']}\n"
    if len(text) > 4096:
        filename = "gbanlist.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(text))
    
            return await m.reply_document(
        document=filename)
    else:
        await m.reply_text(text)
    
    
         
def __stats__():
    return f"• {len(get_gban_list())} ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs."
__mod_name__ = "Gʙᴀɴ​"