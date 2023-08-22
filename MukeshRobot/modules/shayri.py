"""MIT License

Copyright (c) 2023-24 Noob-Mukesh

          GITHUB: NOOB-MUKESH
          TELEGRAM: @MR_SUKKUN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import random, asyncio

from MukeshRobot import pbot
from pyrogram import filters


loveShayri = [
    "Meri chahat dekhni hai? \nTo mere dil par apna dil rakhkar dekh\nteri dhadkan naa bhadjaye to meri mohabbat thukra dena...",
    "Tere ishq me is tarah mai neelam ho jao\naakhri ho meri boli aur main tere naam ho jau...",
    "Nhi pta ki wo kabhi meri thi bhi ya nhi\nmujhe ye pta hai bas ki mai to tha umr bas usi ka rha...",
    "Tumne dekha kabhi chand se pani girte hue\nmaine dekha ye manzar tu me chehra dhote hue...",
    "Tera pata nahi par mera dil kabhi taiyar nahi hoga\nmujhe tere alawa kabi kisi aur se pyaar nhi hoga...",
    "Lga ke phool haathon se usne kaha chupke se\nagar yaha koi nahi hota to phool ki jagah tum hote...",
    "Udas shamo me wo lout\nKar aana bhul jate hain..❤️\nKar ke khafa mujhko wo\nManana bhul jate hain....💞😌",
    "Chalo phir yeha se ghar kaise jaoge...?\n\n🙂🔪Ye humare akhri mulakat h kuch kehna chahoge?🙃❤️\n😔❤️M to khr khel rhi thi tum to sacha isq karte the na😓🔪\nKaise karte karke dekhau..😷🤧\n🤒❤️Tum to kehte the m bichrungi to mar jaooge marke dekhau😖❤️\n😌✨Ek bhola bhala khelta huya dil tut gyi na....🙂❤️\n👀❤️....Ladka chup kyu pata ..?\n😊❤️ ....ladki to margyi naa",
    "Toote huye dil ne bhi uske liye dua\n maangi,\nmeri har saans ne uske liye khushi\n maangi,\nna jaane kaisi dillagi thi uss bewafa se,\naakhiri khwahish mein bhi uski hi wafa maangi.........✍\n\n~ ♡",
    "Main waqt ban jaaun tu ban jaana koi \nlamha, \nMain tujhnme gujar jaaun tu mujhme gujar \njana............✍ \n\n~ ♡ 💘",
    "Udaas lamhon 😞 ki na koi yaad\nrakhna, \ntoofan mein bhi wajood apna sambhal\nRakhna,\nkisi ki zindagi ki khushi ho tum,\n🥰  bs yehi soch tum apna khayal\nRkhna,\n\n~ ♡ 💘❤️",
]
love = random.choice(loveShayri)

@pbot.on_message(filters.command("loveshayri"))

async def love_shayri(b,m):
    "dont remove this line \n credit  |n github : noob-mukesh"
    await m.reply_text(love)
__mod_name__="​​ꜱʜᴀʏʀɪ"
__help__="""ꜱᴇɴᴅ ʀᴀɴᴅᴏᴍ ꜱʜᴀʏʀɪ
❍ /loveshayri : ʟᴏᴠᴇ ꜱʜᴀʏʀɪ"""
