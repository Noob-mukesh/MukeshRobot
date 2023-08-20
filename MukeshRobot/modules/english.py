import json

import requests
from PyDictionary import PyDictionary
from telethon import *
from telethon.tl.types import *

from MukeshRobot.events import register

API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


@register(pattern="^/spell(?: |$)(.*)")
async def _(event):
    ctext = await event.get_reply_message()
    msg = ctext.text
    #  print (msg)
    params = dict(lang="US", clientVersion="2.0", apiKey=API_KEY, text=msg)

    res = requests.get(URL, params=params)
    changes = json.loads(res.text).get("LightGingerTheTextResult")
    curr_string = ""
    prev_end = 0

    for change in changes:
        start = change.get("From")
        end = change.get("To") + 1
        suggestions = change.get("Suggestions")
        if suggestions:
            sugg_str = suggestions[0].get("Text")
            curr_string += msg[prev_end:start] + sugg_str
            prev_end = end

    curr_string += msg[prev_end:]
    await event.reply(curr_string)


dictionary = PyDictionary()


@register(pattern="^/define")
async def _(event):
    text = event.text[len("/define ") :]
    word = f"{text}"
    let = dictionary.meaning(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)


@register(pattern="^/synonyms")
async def _(event):
    text = event.text[len("/synonyms ") :]
    word = f"{text}"
    let = dictionary.synonym(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)


@register(pattern="^/antonyms")
async def _(event):
    text =event.text[len("/antonyms ") :]
    word = f"{text}"
    let = dictionary.antonym(word)
    set = str(let)
    jet = set.replace("{", "")
    net = jet.replace("}", "")
    got = net.replace("'", "")
    await event.reply(got)


__help__ = """
 ❍ /define  <ᴛᴇxᴛ>*:* ᴛʏᴘᴇ ᴛʜᴇ ᴡᴏʀᴅ ᴏʀ ᴇxᴘʀᴇssɪᴏɴ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴇᴀʀᴄʜ\ɴғᴏʀ ᴇxᴀᴍᴘʟᴇ /ᴅᴇғɪɴᴇ ᴋɪʟʟ
 ❍ /spell *:* ᴡʜɪʟᴇ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ, ᴡɪʟʟ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴀ ɢʀᴀᴍᴍᴀʀ ᴄᴏʀʀᴇᴄᴛᴇᴅ ᴠᴇʀsɪᴏɴ
 ❍ /synonyms  <ᴡᴏʀᴅ>*:* ғɪɴᴅ ᴛʜᴇ sʏɴᴏɴʏᴍs ᴏғ ᴀ ᴡᴏʀᴅ
 ❍ /antonyms  <ᴡᴏʀᴅ>*:* ғɪɴᴅ ᴛʜᴇ ᴀɴᴛᴏɴʏᴍs ᴏғ ᴀ ᴡᴏʀᴅ
"""

__mod_name__ = "Eɴɢʟɪsʜ"
