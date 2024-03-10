
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = "17250424" # integer value, dont use ""
    API_HASH = "753bc98074d420ef57ddf7eb1513162b"
    TOKEN = "6963676906:AAEoorPDGfKXX4RAy4iGPTE88s5GCfWmqA4"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1786144151 # If you dont know, run the bot and do /id in your private chat with it, also an integer
    
    SUPPORT_CHAT = "https://t.me/Mikisupport"  # Your own group for support, do not add the @
    START_IMG = "https://telegra.ph//file/af697610484dda54fdbc7.jpg"
    EVENT_LOGS = ()  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    MONGO_DB_URI= "mongodb+srv://tumbuhan:1234@cluster0.qmwnf0b.mongodb.net/?retryWrites=true&w=majority"
    # RECOMMENDED
    DATABASE_URL = "Google Compute Engine asia-east2 (Hong Kong) "  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        "Y9J0CEIQ2NCVN0BC"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "HFHHDLWNTS5Y"
    
    # Get your API key from https://timezonedb.com/api
    API_KEY="29719cd6-7f86-4dad-b00f-3a3738b4005b"
    #generate api from telegram using /token command bot username :>> @adventure_robot

    # Optional fields
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
