import random

from telegram import Update
from telegram.ext import CallbackContext

import MukeshRobot.modules.truth_and_dare_string as truth_and_dare_string
from MukeshRobot import dispatcher
from MukeshRobot.modules.disable import DisableAbleCommandHandler


def truth(update: Update, context: CallbackContext):
    context.args
    update.effective_message.reply_text(random.choice(truth_and_dare_string.TRUTH))


def dare(update: Update, context: CallbackContext):
    context.args
    update.effective_message.reply_text(random.choice(truth_and_dare_string.DARE))


TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)

__help__ = """
*Truth & Dare*
 ❍ /truth *:* Sends a random truth string.
 ❍ /dare *:* Sends a random dare string.
"""
__mod_name__ = "ꜰᴜɴ🔺"
