import requests
from .. import pbot as Mukesh,BOT_NAME,BOT_USERNAME
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
@Mukesh.on_message(filters.command(["password"]))
async def passwordgen(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Example:**\n\n`/password <length>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/password?num={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"Here is your Password:- ` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")
@Mukesh.on_message(filters.command(["morseencode"]))
async def morse_en(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Example:**\n\n`/morseencode <query>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/encode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")
@Mukesh.on_message(filters.command("morsedecode"))
async def morse_de(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Example:**\n\n`/morsedecode <query>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/morse/decode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"`{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")
@Mukesh.on_message(filters.command(["encode"]))
async def base_en(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Example:**\n\n`/encode <query>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/encode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f"` {x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")
@Mukesh.on_message(filters.command(["decode"]))
async def base_de(bot, message):
    
    try:
        
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        if len(message.command) < 2:
            return await message.reply_text(
            "Example:**\n\n`/decode <query>`")
        else:
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://mukesh-api.vercel.app/base/decode?query={a}') 
            x=response.json()["results"]
            
            await message.reply_text(f" `{x}`", parse_mode=ParseMode.MARKDOWN)     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ: {e} ")                                
