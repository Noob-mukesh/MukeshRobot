from os import remove
from pyrogram import filters

from MukeshRobot import DRAGONS, BOT_USERNAME, arq, pbot
from MukeshRobot.utils.errors import capture_err
from MukeshRobot.utils.permissions import adminsOnly
from MukeshRobot.modules.mongo.nsfw_mongo import is_nsfw_on, nsfw_off, nsfw_on


async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@pbot.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
@capture_err
async def detect_nsfw(_, message):
    if not await is_nsfw_on(message.chat.id):
        return
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if message.from_user.id in DRAGONS:
        return
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**ɴsғᴡ ɪᴍᴀɢᴇ ᴅᴇᴛᴇᴄᴛᴇᴅ & ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴇssғᴜʟʟʏ!
————————————————————**
**ᴜsᴇʀ:** {message.from_user.mention} [`{message.from_user.id}`]
**sᴀғᴇ:** `{results.neutral} %`
**ᴘᴏʀɴ:** `{results.porn} %`
**ᴀᴅᴜʟᴛ:** `{results.sexy} %`
**ʜᴇɴᴛᴀɪ:** `{results.hentai} %`
**ᴅʀᴀᴡɪɴɢ:** `{results.drawings} %`
**————————————————————**
__ᴘᴏᴡᴇʀᴇᴅ ʙʏ__@mukeshbotzone.
"""
    )


@pbot.on_message(filters.command(["nsfwscan", f"nsfwscan@{BOT_USERNAME}"]))
@capture_err
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    m = await message.reply_text("Scanning")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Something wrong happened.")
    file = await pbot.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**Neutral:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Hentai:** `{results.hentai} %`
**Sexy:** `{results.sexy} %`
**Drawings:** `{results.drawings} %`
**NSFW:** `{results.is_nsfw}`
"""
    )


@pbot.on_message(filters.command(["antinsfw", f"antinsfw@{BOT_USERNAME}"]) & ~filters.private)
@adminsOnly("can_change_info")
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "Usage: /antinsfw [on/off]"
        )
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status in ("on", "yes"):
        await nsfw_on(chat_id)
        await message.reply_text(
            "Enabled AntiNSFW System. I will Delete Messages Containing Inappropriate Content."
        )
    elif status in ("off", "no"):
        await nsfw_off(chat_id)
        await message.reply_text("Disabled AntiNSFW System.")
    else:
        await message.reply_text(
            "Unknown Suffix, Use /antinsfw [on/off]"
        )
  __mod_name__ = "ɴsғᴡ"
__help__ = f"""
