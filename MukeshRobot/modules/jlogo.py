import random,asyncio,requests,io,os
from pyrogram import filters
from PIL import Image, ImageDraw, ImageFont
from MukeshRobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT,pbot
from pyrogram.enums import ChatAction

LOGO_LINKS = [
    "https://te.legra.ph/file/7345fd37e2ed393b37643.jpg",
    "https://te.legra.ph/file/5ced2c3542ef0662fd6e2.jpg"
    
]


@pbot.on_message(filters.command("jlogo"))
async def jlogo(b,m):
    await b.send_chat_action(m.chat.id, ChatAction.UPLOAD_PHOTO)
    if len(m.command) < 2:
         return await m.reply_text(
            "**Example:**\n\n`/jlogo text`")
    
    pesan = await m.reply("**ᴄʀᴇᴀᴛɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ  ʟᴀᴛᴇsᴛ ʟᴏɢᴏ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ sᴇᴄ...**")
    try:
        text = m.text.split(' ',1)[1]
        randc = random.choice(LOGO_LINKS)
        img = Image.open(io.BytesIO(requests.get(randc).content))
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        fnt = "./MukeshRobot/resources/fonts/UrbanJungleDEMO.otf"

        font = ImageFont.truetype(fnt, 120)
        bbox= draw.textbbox((0,0),text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        h += int(h * 0.21)
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        image_width, image_height = img.size
        draw.text(
            ((image_widthz - w) / 2, (image_heightz - h) / 2),
            text,
            font=font,
            fill=(255, 255, 255),
        )
        x = (image_widthz - w) / 2
        y = (image_heightz - h) / 2 + 6
        draw.text(
            (x, y), text, font=font, fill="white", stroke_width=1, stroke_fill="black"
        )
        fname = "mukesh.png"
        img.save(fname, "png")
        await telethn.send_file(
            event.chat_id,
            file=fname,
            caption=f"""━━━━━━━{BOT_NAME}━━━━━━━

☘️ Jʟᴏɢᴏ ᴄʀᴇᴀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ☘️
◈──────────────◈
🔥 ᴄʀᴇᴀᴛᴇᴅ ʙʏ : @{BOT_USERNAME}
━━━━━━━{BOT_NAME}━━━━━━━""",buttons=button_row
)
        await pesan.delete()
        if os.path.exists(fname):
            os.remove(fname)
    except Exception as e:
        await event.reply(f"ᴇʀʀᴏʀ {e}, ʀᴇᴩᴏʀᴛ ᴛʜɪs ᴀᴛ @{SUPPORT_CHAT} ")

__mod_name__ = "Jʟᴏɢᴏ"

__help__ = f"""
@{BOT_USERNAME} ᴄᴀɴ ᴄʀᴇᴀᴛᴇ sᴏᴍᴇ ʙᴇᴀᴜᴛɪғᴜʟ ᴀɴᴅ ᴀᴛᴛʀᴀᴄᴛɪᴠᴇ ᴊᴜɴɢʟᴇ ʟᴏɢᴏ ғᴏʀ ʏᴏᴜʀ ᴘʀᴏғɪʟᴇ ᴘɪᴄs.


❍ /jlogo (Text) *:* ᴄʀᴇᴀᴛᴇ ᴀ ʟᴏɢᴏ ᴏғ ʏᴏᴜʀ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴡɪᴛʜ ʀᴀɴᴅᴏᴍ ᴠɪᴇᴡ.
"""
