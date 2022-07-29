import io
import re
import html
import random
import requests
from MukeshRobot import dispatcher
from telegram import ParseMode, Update, Bot
from MukeshRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async


def truth(update: Update, context: CallbackContext):
    args = context.args
    truth = requests.get("https://api.truthordarebot.xyz/v1/truth").json()
    truth = truth.get("truth")
    update.effective_message.reply_text(truth)


def dare(update: Update, context: CallbackContext):
    args = context.args
    dare = requests.get("https://api.truthordarebot.xyz/v1/dare").json()
    dare = dare.get("dare")
    update.effective_message.reply_text(dare)


TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)

__help__ = """
*Truth & Dare*
 ❍ /truth *:* Sends a random truth string.
 ❍ /dare *:* Sends a random dare string.
"""
__mod_name__ = "Tʀᴜᴛʜ-Dᴀʀᴇ 😶"
