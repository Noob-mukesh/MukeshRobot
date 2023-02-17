
from pyrogram import Client, filters
from MukeshRobot import  pbot as bot



import openai
openai.api_key = "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"


@bot.on_message(filters.command('chatgpt'))
async def chat(bot, message):
    try:
        input = message.text.split(' ', 1)[1]
        resp = openai.Completion.create(
            model='text-davinci-003', prompt=input)
        await message.reply_text(resp.choices[0].text)
    except Exception as e:
        await message.reply_text(f"Error {e}")
__mod_name__ = "ᴄʜᴀᴛɢᴘᴛ🛡️"
__help__ = """
 ©️ ʙʏ ᯾ [ Mᴜᴋᴇsʜ] (t.me/itz_legend_coder)
*ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs*:
» /chatgpt*:* ask any question
"""
