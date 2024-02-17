"""MIT License

Copyright (c) 2023-24 Noob-Mukesh

          GITHUB: NOOB-MUKESH
          TELEGRAM: @MR_SUKKUN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import requests

from MukeshRobot import pbot
from pyrogram import filters


@pbot.on_message(filters.command("loveshayri"))

async def love_shayri(b,m):

    "dont remove this line \n credit  \n github : noob-mukesh"

    love = requests.get("https://mukesh-api.vercel.app/loveshayri").json()["results"]    
    await m.reply_text(love)
          
@pbot.on_message(filters.command("hateshayri"))
async def hate_shayri(b,m):
    "dont remove this line \n credit  \n github : noob-mukesh"
    hate= requests.get("https://mukesh-api.vercel.app/hateshayri").json()["results"]    
    await m.reply_text(hate)   

__mod_name__="​​Sʜᴀʏʀɪ"

__help__="""ꜱᴇɴᴅ ʀᴀɴᴅᴏᴍ ꜱʜᴀʏʀɪ
❍ /loveshayri : ʟᴏᴠᴇ ꜱʜᴀʏʀɪ
❍ /hateshayri : ʜᴀᴛᴇ ꜱʜᴀʏʀɪ"""
