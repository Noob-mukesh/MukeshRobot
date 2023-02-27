import requests

url = "https://iamai.p.rapidapi.com/ask"
import asyncio

from MukeshRobot import telethn
from MukeshRobot.events import register


@register(pattern="Mukesh (.*)")
async def hmm(event):
    test = event.pattern_match.group(1)
    r = ('\n    "consent": true,\n    "ip": "::1",\n    "question": "{}"\n').format(
        test
    )
    k = f"({r})"
    new_string = k.replace("(", "{")
    lol = new_string.replace(")", "}")
    payload = lol
    headers = {
        "content-type": "application/json",
        "x-forwarded-for": "<user's ip>",
        "x-rapidapi-key": "f852df3a66msh3e4262943a708abp1a5c61jsn3765e8e9510c",
        "x-rapidapi-host": "iamai.p.rapidapi.com",
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    lodu = response.json()
    result = lodu["message"]["text"]
    if "no no" in result:
        pro = "I am fairly found and I was made by @itz_legend_coder."
        try:
            async with telethn.action(event.chat_id, "typing"):
                await asyncio.sleep(2)
                await event.reply(pro)
        except CFError as e:
            print(e)
    elif "ann" in result:
        pro = "My name is Mukesh"
        try:
            async with telethn.action(event.chat_id, "typing"):
                await asyncio.sleep(2)
                await event.reply(pro)
        except CFError as e:
            print(e)
    else:
        try:
            async with telethn.action(event.chat_id, "typing"):
                await asyncio.sleep(2)
                await event.reply(result)
        except CFError as e:
            print(e)
