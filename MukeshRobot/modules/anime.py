import bs4
import html
import jikanpy
import datetime
import textwrap
import requests
import json

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update)
from telegram.ext import CallbackQueryHandler, CommandHandler, run_async, CallbackContext
from telegram.utils.helpers import mention_html
from pyrogram import filters
from bs4 import BeautifulSoup

from MukeshRobot.modules.helper_funcs.alternate import typing_action
from MukeshRobot.modules.disable import DisableAbleCommandHandler
from MukeshRobot import OWNER_ID, REDIS, dispatcher, pbot


kaizoku_btn = "Kaizoku ☠️"
kayo_btn = "Kayo 🏴‍☠️"
info_btn = "More Info 📕"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"

ANIME_IMG = "https://telegra.ph/file/56b16e6599af473d692f9.gif"
MANGA_IMG = "https://telegra.ph/file/e6b1c11a9cd09a9c0e223.gif"
CHARACTER_IMG = "https://telegra.ph/file/a355b31aa5dfe112605d2.gif"

QUOTES_IMG = (
      "https://i.imgur.com/Iub4RYj.jpg", 
      "https://i.imgur.com/uvNMdIl.jpg", 
      "https://i.imgur.com/YOBOntg.jpg", 
      "https://i.imgur.com/fFpO2ZQ.jpg", 
      "https://i.imgur.com/f0xZceK.jpg", 
      "https://i.imgur.com/RlVcCip.jpg", 
      "https://i.imgur.com/CjpqLRF.jpg", 
      "https://i.imgur.com/8BHZDk6.jpg", 
      "https://i.imgur.com/8bHeMgy.jpg", 
      "https://i.imgur.com/5K3lMvr.jpg", 
      "https://i.imgur.com/NTzw4RN.jpg", 
      "https://i.imgur.com/wJxryAn.jpg", 
      "https://i.imgur.com/9L0DWzC.jpg", 
      "https://i.imgur.com/sBe8TTs.jpg", 
      "https://i.imgur.com/1Au8gdf.jpg", 
      "https://i.imgur.com/28hFQeU.jpg", 
      "https://i.imgur.com/Qvc03JY.jpg", 
      "https://i.imgur.com/gSX6Xlf.jpg", 
      "https://i.imgur.com/iP26Hwa.jpg", 
      "https://i.imgur.com/uSsJoX8.jpg", 
      "https://i.imgur.com/OvX3oHB.jpg", 
      "https://i.imgur.com/JMWuksm.jpg", 
      "https://i.imgur.com/lhM3fib.jpg", 
      "https://i.imgur.com/64IYKkw.jpg", 
      "https://i.imgur.com/nMbyA3J.jpg", 
      "https://i.imgur.com/7KFQhY3.jpg", 
      "https://i.imgur.com/mlKb7zt.jpg", 
      "https://i.imgur.com/JCQGJVw.jpg", 
      "https://i.imgur.com/hSFYDEz.jpg", 
      "https://i.imgur.com/PQRjAgl.jpg", 
      "https://i.imgur.com/ot9624U.jpg", 
      "https://i.imgur.com/iXmqN9y.jpg", 
      "https://i.imgur.com/RhNBeGr.jpg", 
      "https://i.imgur.com/tcMVNa8.jpg", 
      "https://i.imgur.com/LrVg810.jpg", 
      "https://i.imgur.com/TcWfQlz.jpg", 
      "https://i.imgur.com/muAUdvJ.jpg", 
      "https://i.imgur.com/AtC7ZRV.jpg", 
      "https://i.imgur.com/sCObQCQ.jpg", 
      "https://i.imgur.com/AJFDI1r.jpg", 
      "https://i.imgur.com/TCgmRrH.jpg", 
      "https://i.imgur.com/LMdmhJU.jpg", 
      "https://i.imgur.com/eyyax0N.jpg", 
      "https://i.imgur.com/YtYxV66.jpg", 
      "https://i.imgur.com/292w4ye.jpg", 
      "https://i.imgur.com/6Fm1vdw.jpg", 
      "https://i.imgur.com/2vnBOZd.jpg", 
      "https://i.imgur.com/j5hI9Eb.jpg", 
      "https://i.imgur.com/cAv7pJB.jpg", 
      "https://i.imgur.com/jvI7Vil.jpg", 
      "https://i.imgur.com/fANpjsg.jpg", 
      "https://i.imgur.com/5o1SJyo.jpg", 
      "https://i.imgur.com/dSVxmh8.jpg", 
      "https://i.imgur.com/02dXlAD.jpg", 
      "https://i.imgur.com/htvIoGY.jpg", 
      "https://i.imgur.com/hy6BXOj.jpg", 
      "https://i.imgur.com/OuwzNYu.jpg", 
      "https://i.imgur.com/L8vwvc2.jpg", 
      "https://i.imgur.com/3VMVF9y.jpg", 
      "https://i.imgur.com/yzjq2n2.jpg", 
      "https://i.imgur.com/0qK7TAN.jpg", 
      "https://i.imgur.com/zvcxSOX.jpg", 
      "https://i.imgur.com/FO7bApW.jpg", 
      "https://i.imgur.com/KK06gwg.jpg", 
      "https://i.imgur.com/6lG4tsO.jpg",
      )

def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f"\n*Description*: {description}[Read More]({info})"
    else:
        msg += f"\n*Description*: {description}"
    return msg


#time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


airing_query = '''
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        siteUrl
        episodes
        title {
          romaji
          english
          native
        }
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
    '''

fav_query = """
query ($id: Int) {
      Media (id: $id, type: ANIME) {
        id
        title {
          romaji
          english
          native
        }
        siteUrl
     }
}
"""

anime_query = '''
   query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''
character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

url = 'https://graphql.anilist.co'



@typing_action
def airing(update, context):
    message = update.effective_message
    search_str = message.text.split(' ', 1)
    if len(search_str) == 1:
        update.effective_message.reply_text(
            '*Usage:* `/airing <anime name>`',
            parse_mode = ParseMode.MARKDOWN)
        return
    variables = {'search': search_str[1]}
    response = requests.post(
        url, json={
            'query': airing_query,
            'variables': variables
        }).json()['data']['Media']
    info = response.get('siteUrl')
    image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
    msg = f"*Name*: *{response['title']['romaji']}*(`{response['title']['native']}`)\n*• ID*: `{response['id']}`[⁠ ⁠]({image})"
    if response['nextAiringEpisode']:
        time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        time = t(time)
        msg += f"\n*Episode*: `{response['nextAiringEpisode']['episode']}`\n*• Airing In*: `{time}`"
    else:
        msg += f"\n*Episode*:{response['episodes']}\n*• Status*: `N/A`"
    update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)



@typing_action
def anime(update, context):
    message = update.effective_message
    search = message.text.split(' ', 1)
    if len(search) == 1:
        update.effective_message.reply_animation(ANIME_IMG, caption="""Format : /anime < anime name >""", parse_mode="markdown")
        return
    else:
        search = search[1]
    variables = {'search': search}
    json = requests.post(
        url, json={
            'query': anime_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        update.effective_message.reply_text('Anime not found ;-;')
        return
    if json:
        json = json['data']['Media']
        msg = f"*{json['title']['romaji']}* *-* *({json['title']['native']})*\n\n*• Type*: {json['format']}\n*• Status*: {json['status']}\n*• Episodes*: {json.get('episodes', 'N/A')}\n*• Duration*: {json.get('duration', 'N/A')} Per Ep.\n*• Score*: {json['averageScore']}\n*• Genres*: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "*• Studios*: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        anime_name_w = f"{json['title']['romaji']}"
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A').replace('<b>', '').replace(
            '</b>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
        if trailer:
            buttons = [[
                InlineKeyboardButton("More Info ➕", url=info),
                InlineKeyboardButton("Trailer 🎬", url=trailer)
            ]]
            buttons += [[InlineKeyboardButton("➕ Add To Watchlist ➕", callback_data=f"xanime_watchlist={anime_name_w}")]]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info)]]
            buttons += [[InlineKeyboardButton("➕ Add To Watchlist", callback_data=f"xanime_watchlist={anime_name_w}")]]
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))



@typing_action
def character(update, context):
    message = update.effective_message
    search = message.text.split(' ', 1)
    if len(search) == 1:
        update.effective_message.reply_animation(CHARACTER_IMG, caption="""Format : /character < character name >""", parse_mode="markdown")
        return
    search = search[1]
    variables = {'query': search}
    json = requests.post(
        url, json={
            'query': character_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        update.effective_message.reply_text('Character not found')
        return
    if json:
        json = json['data']['Character']
        msg = f"* {json.get('name').get('full')}*(`{json.get('name').get('native')}`) \n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        char_name = f"{json.get('name').get('full')}"
        msg += shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            buttons = [[InlineKeyboardButton("Save as Waifu ❣️", callback_data=f"xanime_fvrtchar={char_name}")]]
            update.effective_message.reply_photo(
                photo=image,
                caption=msg.replace('<b>', '</b>'),
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.MARKDOWN)
        else:
            update.effective_message.reply_text(
                msg.replace('<b>', '</b>'), reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN)



@typing_action
def manga(update, context):
    message = update.effective_message
    search = message.text.split(' ', 1)
    if len(search) == 1:
        update.effective_message.reply_animation(MANGA_IMG, caption="""Format : /manga < manga name >""", parse_mode="markdown")
        return
    search = search[1]
    variables = {'search': search}
    json = requests.post(
        url, json={
            'query': manga_query,
            'variables': variables
        }).json()
    msg = ''
    if 'errors' in json.keys():
        update.effective_message.reply_text('Manga not found')
        return
    if json:
        json = json['data']['Media']
        title, title_native = json['title'].get('romaji',
                                                False), json['title'].get(
                                                    'native', False)
        start_date, status, score = json['startDate'].get(
            'year', False), json.get('status',
                                     False), json.get('averageScore', False)
        if title:
            msg += f"*{title}*"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n*Start Date* - `{start_date}`"
        if status:
            msg += f"\n*Status* - `{status}`"
        if score:
            msg += f"\n*Score* - `{score}`"
        msg += '\n*Genres* - '
        for x in json.get('genres', []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json['siteUrl']
        buttons = [[InlineKeyboardButton("More Info", url=info)]]
        buttons += [[InlineKeyboardButton("📕 Add To Read List", callback_data=f"xanime_manga={title}")]]
        image = json.get("bannerImage", False)
        msg += f"_{json.get('description', None)}_"
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))



@typing_action
def user(update, context):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)

    try:
        search_query = args[1]
    except:
        if message.reply_to_message:
            search_query = message.reply_to_message.text
        else:
            update.effective_message.reply_text("Format : /user <username>")
            return

    jikan = jikanpy.jikan.Jikan()

    try:
        user = jikan.user(search_query)
    except jikanpy.APIException:
        update.effective_message.reply_text("Username not found.")
        return

    progress_message = update.effective_message.reply_text("Searching.... ")

    date_format = "%Y-%m-%d"
    if user['image_url'] is None:
        img = "https://cdn.myanimelist.net/images/questionmark_50.gif"
    else:
        img = user['image_url']

    try:
        user_birthday = datetime.datetime.fromisoformat(user['birthday'])
        user_birthday_formatted = user_birthday.strftime(date_format)
    except:
        user_birthday_formatted = "Unknown"

    user_joined_date = datetime.datetime.fromisoformat(user['joined'])
    user_joined_date_formatted = user_joined_date.strftime(date_format)

    for entity in user:
        if user[entity] is None:
            user[entity] = "Unknown"

    about = user['about'].split(" ", 60)

    try:
        about.pop(60)
    except IndexError:
        pass

    about_string = ' '.join(about)
    about_string = about_string.replace("<br>",
                                        "").strip().replace("\r\n", "\n")

    caption = ""

    caption += textwrap.dedent(f"""
    *Username*: [{user['username']}]({user['url']})
    *Gender*: `{user['gender']}`
    *Birthday*: `{user_birthday_formatted}`
    *Joined*: `{user_joined_date_formatted}`
    *Days wasted watching anime*: `{user['anime_stats']['days_watched']}`
    *Days wasted reading manga*: `{user['manga_stats']['days_read']}`
    """)

    caption += f"*About*: {about_string}"

    buttons = [[InlineKeyboardButton(info_btn, url=user['url'])],
               [
                   InlineKeyboardButton(
                       close_btn,
                       callback_data=f"anime_close, {message.from_user.id}")
               ]]

    update.effective_message.reply_photo(
        photo=img,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=False)
    progress_message.delete()



@typing_action
def upcoming(update, context):
    jikan = jikanpy.jikan.Jikan()
    upcoming = jikan.top('anime', page=1, subtype="upcoming")

    upcoming_list = [entry['title'] for entry in upcoming['top']]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    update.effective_message.reply_text(upcoming_message)


def watchlist(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message  
    watchlist = list(REDIS.sunion(f'anime_watch_list{user.id}'))
    watchlist.sort()
    watchlist = "\n• ".join(watchlist)
    if watchlist:
        message.reply_text(
            "{}<b>'s Watchlist:</b>"
            "\n• {}".format(mention_html(user.id, user.first_name),
                        watchlist),
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            "You havn't added anything in your watchlist!"
        )

def removewatchlist(update, context):
    user = update.effective_user 
    message = update.effective_message 
    removewlist = message.text.split(' ', 1) 
    args = context.args
    query = " ".join(args)
    if not query:
        message.reply_text("Please enter a anime name to remove from your watchlist.")
        return
    watchlist = list(REDIS.sunion(f'anime_watch_list{user.id}'))
    removewlist = removewlist[1]
    
    if removewlist not in watchlist:
        message.reply_text(
            f"<code>{removewlist}</code> doesn't exist in your watch list.",
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            f"<code>{removewlist}</code> has been removed from your watch list.",
            parse_mode=ParseMode.HTML
        )
        REDIS.srem(f'anime_watch_list{user.id}', removewlist)


def fvrtchar(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message  
    fvrt_char = list(REDIS.sunion(f'anime_fvrtchar{user.id}'))
    fvrt_char.sort()
    fvrt_char = "\n• ".join(fvrt_char)
    if fvrt_char:
        message.reply_text(
            "{}<b>'s Harem:</b>"
            "\n• {}".format(mention_html(user.id, user.first_name),
                        fvrt_char),
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            "You havn't added any waifu in your harem!"
        )
        

def removefvrtchar(update, context):
    user = update.effective_user 
    message = update.effective_message 
    removewlist = message.text.split(' ', 1) 
    args = context.args
    query = " ".join(args)
    if not query:
        message.reply_text("Please enter a your waifu name to remove from your harem.")
        return
    fvrt_char = list(REDIS.sunion(f'anime_fvrtchar{user.id}'))
    removewlist = removewlist[1]
    
    if removewlist not in fvrt_char:
        message.reply_text(
            f"<code>{removewlist}</code> doesn't exist in your harem",
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            f"<code>{removewlist}</code> has been removed from your harem",
            parse_mode=ParseMode.HTML
        )
        REDIS.srem(f'anime_fvrtchar{user.id}', removewlist)
    

def readmanga(update, context):
    chat = update.effective_chat  
    user = update.effective_user 
    message = update.effective_message  
    manga_list = list(REDIS.sunion(f'anime_mangaread{user.id}'))
    manga_list.sort()
    manga_list = "\n• ".join(manga_list)
    if manga_list:
        message.reply_text(
            "{}<b>'s Manga Lists:</b>"
            "\n• {}".format(mention_html(user.id, user.first_name),
                        manga_list),
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            "You havn't added anything in your manga list!"
        )


def removemangalist(update, context):
    user = update.effective_user 
    message = update.effective_message 
    removewlist = message.text.split(' ', 1) 
    args = context.args
    query = " ".join(args)
    if not query:
        message.reply_text("Please enter a manga name to remove from your manga list.")
        return
    fvrt_char = list(REDIS.sunion(f'anime_mangaread{user.id}'))
    removewlist = removewlist[1]
    
    if removewlist not in fvrt_char:
        message.reply_text(
            f"<code>{removewlist}</code> doesn't exist in your manga list.",
            parse_mode=ParseMode.HTML
        )
    else:
        message.reply_text(
            f"<code>{removewlist}</code> has been removed from your favorite characters list.",
            parse_mode=ParseMode.HTML
        )
        REDIS.srem(f'anime_mangaread{user.id}', removewlist)

def animestuffs(update, context):
    query = update.callback_query
    user = update.effective_user
    splitter = query.data.split('=')
    query_match = splitter[0]
    callback_anime_data = splitter[1] 
    if query_match == "xanime_watchlist":
        watchlist = list(REDIS.sunion(f'anime_watch_list{user.id}'))
        if not callback_anime_data in watchlist:
            REDIS.sadd(f'anime_watch_list{user.id}', callback_anime_data)
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is successfully added to your watch list.",
                                                show_alert=True)
        else:
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is already exists in your watch list!",
                                                show_alert=True)
            
    elif query_match == "xanime_fvrtchar":   
        fvrt_char = list(REDIS.sunion(f'anime_fvrtchar{user.id}'))
        if not callback_anime_data in fvrt_char:
            REDIS.sadd(f'anime_fvrtchar{user.id}', callback_anime_data)
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is successfully added to your favorite character.",
                                                show_alert=True)
        else:
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is already exists in your favorite characters list!",
                                                show_alert=True)
    elif query_match == "xanime_manga":   
        fvrt_char = list(REDIS.sunion(f'anime_mangaread{user.id}'))
        if not callback_anime_data in fvrt_char:
            REDIS.sadd(f'anime_mangaread{user.id}', callback_anime_data)
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is successfully added to your favorite character.",
                                                show_alert=True)
        else:
            context.bot.answer_callback_query(query.id,
                                                text=f"{callback_anime_data} is already exists in your favorite characters list!",
                                                show_alert=True)

def button(update, context):
    bot = context.bot
    query = update.callback_query
    message = query.message
    data = query.data.split(", ")
    query_type = data[0]
    original_user_id = int(data[1])

    user_and_admin_list = [original_user_id, OWNER_ID] + DRAGONS + DEV_USERS

    bot.answer_callback_query(query.id)
    if query_type == "anime_close":
        if query.from_user.id in user_and_admin_list:
            message.delete()
        else:
            query.answer("You are not allowed to use this.")
    elif query_type in ('anime_anime', 'anime_manga'):
        mal_id = data[2]
        if query.from_user.id == original_user_id:
            message.delete()
            progress_message = bot.sendMessage(message.chat.id,
                                               "Searching.... ")
            caption, buttons, image = get_anime_manga(mal_id, query_type,
                                                      original_user_id)
            bot.sendPhoto(
                message.chat.id,
                photo=image,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=False)
            progress_message.delete()
        else:
            query.answer("You are not allowed to use this.")

def anime_quote():
    url = "https://animechan.vercel.app/api/random"
    # since text attribute returns dictionary like string
    response = requests.get(url)
    try:
        dic = json.loads(response.text)
    except Exception:
        pass
    quote = dic["quote"]
    character = dic["character"]
    anime = dic["anime"]
    return quote, character, anime


def quotes(update: Update, context: CallbackContext):
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change🔁", callback_data="change_quote")]]
    )
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )


def change_quote(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    quote, character, anime = anime_quote()
    msg = f"<i>❝{quote}❞</i>\n\n<b>{character} from {anime}</b>"
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="Change🔁", callback_data="quote_change")]]
    )
    message.edit_text(msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)

def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    search_query = extract_arg(message)
    more_results = True

    if not search_query:
        message.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KaizokuAnime: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KaizokuAnime"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KayoAnime: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> @KayoAnime"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    else:
        message.reply_text(
            result, parse_mode=ParseMode.HTML, disable_web_page_preview=True,
        )



def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")



def kayo(update: Update, context: CallbackContext):
    site_search(update, context, "kayo")

def animequotes(update: Update, context: CallbackContext):
    message = update.effective_message
    name = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    reply_photo = message.reply_to_message.reply_photo if message.reply_to_message else message.reply_photo
    reply_photo(
        random.choice(QUOTES_IMG))
      
@pbot.on_message(filters.command('watchorder'))
def watchorderx(_,message):
	anime =  message.text.replace(message.text.split(' ')[0], '')
	res = requests.get(f'https://chiaki.site/?/tools/autocomplete_series&term={anime}').json()
	data = None
	id_ = res[0]['id']
	res_ = requests.get(f'https://chiaki.site/?/tools/watch_order/id/{id_}').text
	soup = BeautifulSoup(res_ , 'html.parser')
	anime_names = soup.find_all('span' , class_='wo_title')
	for x in anime_names:
		data = f"{data}\n{x.text}" if data else x.text
	message.reply_text(f'Watchorder of {anime}: \n```{data}```')

__help__ = """
Get information about anime, manga or characters from [AniList](anilist.co)
*AniList Commands:*
  ➢ `/anime <anime>`*:* returns information about the anime from AniList.
  ➢ `/character <character>`*:* returns information about the character from AniList.
  ➢ `/manga <manga>`*:* returns information about the manga from AniList.
  ➢ `/upcoming`*:* returns a list of new anime in the upcoming seasons from AniList.
  ➢ `/airing <anime>`*:* returns anime airing info from AniList.
 
Get information about anime, manga or characters from [MAL](https://myanimelist.net/)
*My Anime list Commands:*
  ➢ `/manime <anime>`*:* returns information about the anime MAL.
  ➢ `/mcharacter` <character>*:* returns information about the character from MAL.
  ➢ `/mmanga <manga>`*:* returns information about the manga from MAL.
  ➢ `/mupcoming`*:* returns a list of new anime in the upcoming seasons from MAL.
  ➢ `/user <user>`*:* returns information about a MyAnimeList user.
  ➢ `/animequotes`*:* sends random anime quotes.

*Anime Search Commands:*
   ➢ `/kayo`*:* search an Anime on AnimeKayo website.
   ➢ `/kaizoku`*:* search an Anime on AnimeKaizoku website.
   ➢ `/whatanime`*:* Please reply to a Gif or Photo or Video, then bot gives information about the anime.
   
*Anime Search Commands:*
  ➢ `/meme`*:* sends Anime Memes.
  ➢ `/hmeme`*:* sends Hentai Memes.
  ➢ `/rmeme`*:* sends Reddit Memes.
  
*Anime Search Commands:*
  ➢ `/watchorder <anime>`*:* send watch Order of anime.
  
You saw a good anime video, photo, gif but dont know what is that anime's name?
This is where whatanime comes in, just reply to that media with /whatanime and it will search the anime name for you from anilist.                             
 """

ANIME_HANDLER = DisableAbleCommandHandler("anime", anime, run_async=True)
AIRING_HANDLER = DisableAbleCommandHandler("airing", airing, run_async=True)
CHARACTER_HANDLER = DisableAbleCommandHandler("character", character, run_async=True)
MANGA_HANDLER = DisableAbleCommandHandler("manga", manga, run_async=True)
USER_HANDLER = DisableAbleCommandHandler("user", user, run_async=True)
UPCOMING_HANDLER = DisableAbleCommandHandler("upcoming", upcoming, run_async=True)
KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku, run_async=True)
KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo, run_async=True)
BUTTON_HANDLER = CallbackQueryHandler(button, pattern='anime_.*', run_async=True)
WATCHLIST_HANDLER = DisableAbleCommandHandler("watchlist", watchlist, run_async=True)
MANGALIST_HANDLER = DisableAbleCommandHandler("mangalist", readmanga, run_async=True)
FVRT_CHAR_HANDLER = DisableAbleCommandHandler(["characterlist","fcl","mywaifus"], fvrtchar, run_async=True)
REMOVE_WATCHLIST_HANDLER = DisableAbleCommandHandler(["removewatchlist","rwl"], removewatchlist, run_async=True)
REMOVE_FVRT_CHAR_HANDLER = DisableAbleCommandHandler(["rfcharacter","rfcl"], removefvrtchar, run_async=True)
REMOVE_MANGA_CHAR_HANDLER = DisableAbleCommandHandler(["rmanga","rml"], removemangalist, run_async=True)
BUTTON_HANDLER = CallbackQueryHandler(button, pattern='anime_.*', run_async=True)
ANIME_STUFFS_HANDLER = CallbackQueryHandler(animestuffs, pattern='xanime_.*', run_async=True)
ANIMEQUOTES_HANDLER = DisableAbleCommandHandler("animequotes", animequotes, run_async=True)
QUOTE = DisableAbleCommandHandler("quote", quotes)
CHANGE_QUOTE = CallbackQueryHandler(change_quote, pattern=r"change_.*", run_async=True)
QUOTE_CHANGE = CallbackQueryHandler(change_quote, pattern=r"quote_.*", run_async=True)


dispatcher.add_handler(BUTTON_HANDLER)
dispatcher.add_handler(ANIME_HANDLER)
dispatcher.add_handler(ANIME_STUFFS_HANDLER)
dispatcher.add_handler(CHARACTER_HANDLER)
dispatcher.add_handler(MANGA_HANDLER)
dispatcher.add_handler(AIRING_HANDLER)
dispatcher.add_handler(USER_HANDLER)
dispatcher.add_handler(UPCOMING_HANDLER)
dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(WATCHLIST_HANDLER)
dispatcher.add_handler(MANGALIST_HANDLER)
dispatcher.add_handler(FVRT_CHAR_HANDLER)
dispatcher.add_handler(REMOVE_FVRT_CHAR_HANDLER)
dispatcher.add_handler(REMOVE_MANGA_CHAR_HANDLER)
dispatcher.add_handler(REMOVE_WATCHLIST_HANDLER)
dispatcher.add_handler(ANIMEQUOTES_HANDLER)
dispatcher.add_handler(QUOTE)
dispatcher.add_handler(CHANGE_QUOTE)
dispatcher.add_handler(QUOTE_CHANGE)

__mod_name__ = "ᴀɴɪᴍᴇ"
__command_list__ = [
    "anime",
    "manga",
    "character",
    "user",
    "upcoming",
    "airing"
    "kayo",
    "kaizoku",
    "animequotes",
]
__handlers__ = [
    ANIME_HANDLER,
    CHARACTER_HANDLER,
    MANGA_HANDLER,
    USER_HANDLER,
    UPCOMING_HANDLER,
    BUTTON_HANDLER,
    AIRING_HANDLER,
    KAYO_SEARCH_HANDLER,
    KAIZOKU_SEARCH_HANDLER,
    ANIMEQUOTES_HANDLER,
]
