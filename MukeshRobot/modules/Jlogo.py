import glob
import io
import os
import random

import requests
from PIL import Image, ImageDraw, ImageFont

from MukeshRobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT, telethn
from MukeshRobot.events import register

LOGO_LINKS = [
    "https://te.legra.ph/file/7345fd37e2ed393b37643.jpg",
    "https://te.legra.ph/file/5ced2c3542ef0662fd6e2.jpg"
    
]


@register(pattern="^/jlogo ?(.*)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if event.sender_id != OWNER_ID and not quew:
        await event.reply(
            "`ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ʟᴏɢᴏ ʙᴀʙᴇ​ !`\nExample `/jlogo mukesh`"
        )
        return
    pesan = await event.reply("**ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ​...**")
    try:
        text = event.pattern_match.group(1)
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = "./MukeshRobot/resources/fonts/UrbanJungleDEMO.otf"
        randf=fnt
        font = ImageFont.truetype(randf, 150)
        w, h = draw.textsize(text, font=font)
        h += int(h * 0.21)
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2+10
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "mukesh.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f" ɢᴇɴᴇʀᴀᴛᴇᴅ ʙʏ @{BOT_USERNAME}"
)
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)
    except Exception:
        await event.reply(f"ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴇʀʀᴏʀ, ʀᴇᴩᴏʀᴛ ᴛʜɪs ᴀᴛ @{SUPPORT_CHAT}")


__mod_name__ = "⍟ ᴊʟᴏɢᴏ ⍟"

__help__ = """
@{BOT_USERNAME} ᴄᴀɴ ᴄʀᴇᴀᴛᴇ sᴏᴍᴇ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴᴅ ᴀᴛᴛʀᴀᴄᴛɪᴠᴇ ᴊᴜɴɢʟᴇ ʟᴏɢᴏ ғᴏʀ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ᴘɪᴄs.


❍ /flogo (Text) *:* ᴄʀᴇᴀᴛᴇ ᴀ ʟᴏɢᴏ ᴏғ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ᴠɪᴇᴡ.
"""
