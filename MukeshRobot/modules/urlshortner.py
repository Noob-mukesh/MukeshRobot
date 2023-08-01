from pyrogram import Client, enums, filters, idle

import re
from requests import get
import asyncio
from MukeshRobot import pbot as mukesh

from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm, Message
from pyrogram.enums import ChatAction, ParseMode
import pyshorteners
shortener = pyshorteners.Shortener()
from pyrogram.handlers import MessageHandler
@mukesh.on_message(filters.command(["short"]))
async def short_urls(bot, message):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    if len(message.command) < 2:
        return await message.reply_text(
            "**Example:**\n\n`/short [url]`")
#     url_pattern = re.compile(r'https?://\S+')
    link=message.command[1]
#     link = url_pattern.findall(urls)

# Check if any URLs were found
#     if link not in urls:
#                         return	await message.reply_text("this is not valid provide url")
#     else:                         
    try:

        tiny_link = shortener.tinyurl.short(link)


        dagd_link = shortener.dagd.short(link)

        clckru_link = shortener.clckru.short(link)

        shorted=[tiny_link,dagd_link,clckru_link]
        url=[
        [ikb("Tiny Url",url=tiny_link)],

        [ikb("Dagd Url",url=dagd_link),

         ikb("Clckru Url",url=clckru_link)
        ]
        ]
        await message.reply_text(f"Here are few shortened links :",reply_markup=ikm(url))

    except Exception as e:
        await message.reply_text(f"Either the link is already shortened or is invalid.")

@mukesh.on_message(filters.command(["unshort"]))
async def unshort(bot, message):
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    if len(message.command) < 2:
        return await message.reply_text(
            "**Example:**\n\n`/unshort [short - url]`")
    link=message.text.split(' ')[1]
    
    try:

        x = get(link, allow_redirects=True).url

        url=[

        [ikb

         ("View Link",url=x)

        ]

        ]

        

        await message.reply_text(f"Here's the unshortened link :\n`{x}` " ,reply_markup=ikm(url))

        

    except Exception as e:

        await message.reply_text(f"ᴇʀʀᴏʀ:    {e} ")
# mukesh.add_handler(MessageHandler(short_urls))
# mukesh.add_handler(MessageHandler(unshort))
__help__ = """
ᴍᴀᴋᴇ sʜᴏʀᴛs ᴏғ ᴀ ɢɪᴠᴇɴ ʟɪɴᴋ 
 ❍ /short <url>  *:Example `/short https://t.me/mr_sukkun`.
 *"""

__mod_name__ = "Sʜᴏʀᴛᴇɴᴇʀ"
