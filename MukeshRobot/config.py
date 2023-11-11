
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "29538539" # integer value, dont use ""
    API_HASH = "e3141eb87727600cee656cf0cf8007d6"
    TOKEN = "6754559542:AAGK8HroDNaiQgS1aJW_Pdu9fZHjeXJfDdk"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 6230236721 # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "Weebs_GoD"  # Your own group for support, do not add the @
    START_IMG = "https://telegra.ph/Naruto-8-10-27"
    EVENT_LOGS = (-1002004581450)  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    MONGO_DB_URI= "mongodb+srv://mralone:mralone@teamxds.zpsi9fb.mongodb.net/?retryWrites=true&w=majority"
    # RECOMMENDED
    DATABASE_URL = ""  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        "W08HB8232KDEQ0A4"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "K1UZIZ5VJWJL"
    # Get your API key from https://timezonedb.com/api

    # Optional fields
    CHATBOT_API="5935608297-fallen-usbk33kbsu" # get it from @FallenChat_Bot using /token
    BL_CHATS = []  # List of groups that you want blacklisted.
    DRAGONS = []  # User id of sudo users
    DEV_USERS = []  # User id of dev users
    DEMONS = []  # User id of support users
    TIGERS = []  # User id of tiger users
    WOLVES = []  # User id of whitelist users

    ALLOW_CHATS = True
    ALLOW_EXCL = True
    DEL_CMDS = True
    INFOPIC = True
    LOAD = []
    NO_LOAD = []
    STRICT_GBAN = True
    TEMP_DOWNLOAD_DIRECTORY = "./"
    WORKERS = 8
    

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
