#Credit Noob-Mukesh
import random
import asyncio
from pyrogram import filters
from MukeshRobot import pbot as MukeshRobot




wish_STRINGS = [
                     'Happy Rakshabandhan Day',
                     "Thanks for always being my pillar of strength. I am very blessed to have a brother like you. Happy Raksha Bandhan!",
                     "A very big thank you for being my companion, my protector and being equally weird with me. You are the best brother in this world. Happy Raksha Bandhan!",
                     "Happy Raksha Bandhan to my childhood leg-puller, my lovely brother, my guardian and the only person who knows me inside-out. Thanks for always being there. Happy Raksha Bandhan bro!",
                     "I pray for your happiness, prosperity, and long life, sweetest brother. Sending loads of love and best wishes. Happy Raksha Bandhan.",
                     "You are the only person who supports me in my hard times; you are the one who shakes a leg with me in my happiness. There was no single day in my life when you weren't there. I really love you my big brother.",
                     "You supported me while I was in distress; you protected me when I was scared and all other things you did to make me happy. Thanks are just insufficient to express my gratitude. Happy Raksha Bandhan to you Brother!",
                     "Dearest sister, this Raksha Bandhan, I promise to always be your savior and will always be by your side no matter what. Sending loads of blessings and gifts just for you!",
                     "This holy thread you tie on my wrist will strengthen our bond more and fills my heart with more love for you.\n You are the best sis in the world!",
                     "Happy Raksha Bandhan!",
                     "May god bless my angelic sister with loads of happiness, health and success. Happy Raksha Bandhan.",
                     "I wait for the day throughout the year to see you tie a Rakhi so religiously on my wrist and pray to God for my well-being. Sweetest Sis, I wish our bond grows stronger day by day...",
                     "To have an affectionate relationship with a sister is not just to have a friend or a confidant -- it is to have a companion for life.",
                     "Dont wish to @itz_mst_boi .\n I already have my best sis (Swathi).",
                   ]

INDIAN_STRINGS = [
                  "No matter what our religion, in the end, we are all Indians. May our nation become the most prosperous in the world. Happy Independence Day!",
                  "Today I breathe the air of freedom because of the efforts of our great freedom fighters. Happy Independence Day!",
                  "May the Indian tricolour always fly high. Sending you warm wishes on the grand occasion of Independence Day!",
                  "Let’s salute the martyrs For the sacrifices they made, And thank them For giving us our today.",
                  "Today is a day to feel proud about being a part of this great nation. May this spirit of freedom leads us all to success and glory in life. Happy Independence Day!",
                  "We may never know how it feels like to live in a free country if it was not for the bravery of our fathers. Today they deserve a big salute from us. Happy Independence Day!",
                 ]


@MukeshRobot.on_message(filters.command(["Independence", "Indian"]))
async def lel(bot, message):
    ran2 = random.choice(INDIAN_STRINGS)
    await bot.send_chat_action(message.chat.id, "Typing")
    await asyncio.sleep(0.5)
    return await message.reply_text(text=ran2)


@MukeshRobot.on_message(filters.command(["rakhi", "rakshabandhan"]))
async def lel(bot, message):
    ran = random.choice(wish_STRINGS)
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.5)
    return await message.reply_text(text=ran)


__mod_name__ = "ᴡɪsʜ"

__help__ = """

ᴡɪsʜ ʟɪɴᴇ ʙᴀʙʏ
❍ /rakshabandhan *:* ᴡɪsʜ ᴏɴ ғᴇsᴛɪᴠᴀʟ
❍ /rakhi *:* ᴏʀ ᴛʀʏ ᴛʜɪs
❍ /Independence *:*  ɪɴᴅᴇᴘᴇɴᴅᴇɴᴄᴇ ᴅᴀʏ ᴡɪsʜᴇs
❍ /Indian *:* or try Indian
  
 """
