class Config(object):
    LOGGER = True
    API_ID = 24139942
    API_HASH = "89946104c3380aeb322e96bd819d77ea"
    TOKEN = "7705269037:AAFHvns7j6j-kNOuxKI8nZ4Oo_CcI4F2ItA"  
    OWNER_ID=7058301407
    
    SUPPORT_CHAT = "" 
    START_IMG = "https://files.catbox.moe/0wm3s8.jpg"
    EVENT_LOGS = ()
    MONGO_DB_URI= "mongodb+srv://razer:razer@cluster1.4uj5sms.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
   
    DATABASE_URL = ""  # A sql database url from elephantsql.com
    CASH_API_KEY = (
        ""
    )
    TIME_API_KEY = ""

    
    BL_CHATS = [] 
    DRAGONS = []
    DEV_USERS = []  
    DEMONS = [] 
    TIGERS = []  
    WOLVES = [] 

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
