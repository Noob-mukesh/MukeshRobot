
from pyrogram import  filters
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid
from pyrogram.types import ChatPermissions
from pyrogram.enums import ChatMembersFilter
import requests,asyncio
from MukeshRobot import pbot as app,DEV_USERS,OWNER_ID,DEMONS,DRAGONS


OFFICERS = [OWNER_ID] + DEV_USERS + DRAGONS + DEMONS 

# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id or user_id in OFFICERS:
            admin = True
            break
    return admin

@app.on_message(filters.command("zombies", prefixes=["/","!"]) & filters.group)
async def rm_deletedacc(client, message):
    con = message.text.split(" ", 1)[1].lower() if len(message.command) > 1 else ""
    del_u = 0
    del_status = "Group cleaned, 0 deleted accounts found."
    
    if con != "clean":
        kontol = await message.reply("Searching for deleted accounts...")
        
        participants=[]
        async for member in app.get_chat_members(message.chat.id):
            participants.append(member)
        
      
        for user in participants:
            if user.user.is_deleted:
                print(user.user.is_deleted)
                del_u += 1
                await asyncio.sleep(1)
        if del_u > 0:
            del_status = (
                f"Searching... {del_u} Deleted account(s) Zombie on this group, "
                "Clean it with command `/zombies clean`"
            )
        return await kontol.edit(del_status)
    
    chat = await client.get_chat(message.chat.id)
    
    admin=await is_administrator(message.from_user.id,message)
    
    if not admin:
        return await message.reply("Sorry, you are not an admin!")
    
    memek = await message.reply("Removing deleted accounts...")
    participants=[]
    async for member in app.get_chat_members(message.chat.id):
        participants.append(member)
   
    for user in participants:
        if user.user.is_deleted:
            print(user.user.is_deleted)
            try:
                
                await client.ban_chat_member(message.chat.id, user.user.id)
                await client.unban_chat_member(message.chat.id, user.user.id)
                
            except ChatAdminRequired:
                return await message.edit("Do not have permission to ban in this group")
            except UserAdminInvalid:
                del_u -= 1
            await asyncio.sleep(1)
    
    if del_u > 0:
        del_status = f"Cleaned {del_u} Zombies"
    
    await memek.edit(del_status)

help_text = """
*ʀᴇᴍᴏᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀᴄᴄᴏᴜɴᴛs*
❍ /zombies : starts searching for deleted accounts in the group.
❍ /zombies clean : removes the deleted accounts from the group.
"""
__mod_name__ = "Zᴏᴍʙɪᴇ"
