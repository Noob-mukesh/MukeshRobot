import random
import asyncio
from pyrogram import filters
from MukeshRobot import pbot as MukeshRobot




ROMANTIC_STRINGS = [
                     'Meri chahat dekhni hai? \nTo mere dil par apna dil rakhkar dekh\nteri dhadkan naa bhadjaye to meri mohabbat thukra dena...',
                     'Tere ishq me is tarah mai neelam ho jao\naakhri ho meri boli aur main tere naam ho jau...',
                     'Nhi pta ki wo kabhi meri thi bhi ya nhi\nmujhe ye pta hai bas ki mai to tha umr bas usi ka rha...',
                     'Tumne dekha kabhi chand se pani girte hue\nmaine dekha ye manzar tu me chehra dhote hue...',
                     'Tera pata nahi par mera dil kabhi taiyar nahi hoga\nmujhe tere alawa kabi kisi aur se pyaar nhi hoga...',
                     'Lga ke phool haathon se usne kaha chupke se\nagar yaha koi nahi hota to phool ki jagah tum hote...',
                     'Jab Dhadkano Ko Tham Leta Hai Koi\nJab Khayalo Mein Naam Hamara Leta Hai koi,\nYaade Tab aur Yaadgar Ban Jaati Hai,\nJab Hume Humse Behtar Jaan Leta Hai Koi.',
                     'Love is not what the mind thinks, but what the heart feels',
                     'You Smile When You Happy I Smile When I See You Happy.',
                     'Never Forget About The Ones That Love You Back \n @Mukhushi\_official',
                     'Loving The Right Person Will Make You The Strongest And The Most Confident Person.\n @Mukhushi\_official ',
                     'Come live in my heart and pay no rent \n @Mukhushi\_official',
                     'What You Say And What You Do Both Matters When You Are In Love.\n @Mukhushi\_official',
                     'Falling In Love Is Easy But Keeping A Relationship Together Isn’t Easy.\n @Mukhushi\_official',
                     'Start Spreading Love Instead Of Searching For It.\n @Mukhushi\_official',
                     'Love Is In The Purest Form When There Are No Conditions In It.\n @Mukhushi\_official',         
                   ]


@MukeshRobot.on_message(filters.command("romantic"))
async def lel(bot, message):
    ran = random.choice(ROMANTIC_STRINGS)
    await bot.send_chat_action(message.chat.id, "typing")
    await asyncio.sleep(1.5)
    return await message.reply_text(text=ran)

__mod_name__ = "sʜᴀʏᴀʀɪ"

__help__ = """

ᴍᴀᴋᴇs ᴀ sʜᴀʏᴀʀɪ ғᴏʀ ᴜʀ ɢɪʀʟғʀɪᴇɴᴅ ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ.

❍ /romantic *:* ᴡʀɪᴛᴇ sʜᴀʏᴀʀɪ 

 """
