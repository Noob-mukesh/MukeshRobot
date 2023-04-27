import requests
import random
import os
import json
import asyncio
from faker import Faker
from datetime import date
from MukeshRobot import pbot as app 
from pyrogram import filters
@app.on_message(filters.command(["faker"]))
async def gen(bot,msg):
    try:
       fake = Faker()
	    K=fake.profile()
       bhurr = await msg.reply("ɢᴇɴᴇʀᴀᴛɪɴɢ ɪɴꜰᴏ...")
       for i , y in K.items():
        pass
        await bhurr.delete()
        await msg.reply(f"{i} :- {y} ")
    except Exception as e:
        await msg.reply(f"#Error {e}")   
__mod_name__ = "⍟ ғᴀᴋᴇʀ ⍟"
__help__ = """Rᴀɴᴅᴏᴍ Usᴇʀ Iɴғᴏ Gᴇɴᴇʀᴀᴛᴏʀ

ᴜsᴀɢᴇ:
> /faker | Gᴇɴᴇʀᴀᴛᴇs Fᴀᴋᴇ Rᴀɴᴅᴏᴍ Usᴇʀ Iɴғᴏ (ɪᴍᴀɢᴇ ɪs ɢᴇɴᴇʀᴀᴛᴇᴅ ғʀᴏᴍ [ᴛʜɪsᴘᴇʀsᴏɴᴅᴏᴇsɴᴏᴛᴇxɪsᴛ.ᴄᴏᴍ](https://www.thispersondoesnotexist.com/))
"""