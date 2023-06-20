import requests
from bs4 import BeautifulSoup as  BSP
from MukeshRobot import pbot as mukesh

url = "https://all-hashtag.com/library/contents/ajax_generator.php"

@mukesh.on_message(filters.command("hastag"))
async def echo(bot, message):
    global content
    try:
        text = message.text.split(' ',1)[1]
        data = dict(keyword=text, filter="top")

        res = requests.post(url, data).text

        content = BSP(res, 'html.parser').find("div", {"class":"copy-hashtags"}).string
    except IndexError:
        return await message.reply_text("Example:\n\n`/hastag python`")
        
    
    await message.reply_text(f"ʜᴇʀᴇ ɪs ʏᴏᴜʀ  ʜᴀsᴛᴀɢ :\n<pre>{content}</pre>", quote=True,
    


