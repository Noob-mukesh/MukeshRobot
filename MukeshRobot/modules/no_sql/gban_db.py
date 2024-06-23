from MukeshRobot import MONGO_DB_URI
from pymongo import MongoClient

myclient = MongoClient(MONGO_DB_URI)

users =myclient["MUK_users"]

ban_db=users["gban_db"]

# banned db

def is_user_ingbanned(user_id: int) -> bool:
    user = ban_db.find_one({"user_id": user_id})
    if user is not None:  
        return True
    return False

def add_gban(user_id: int, gban_reason: str = None):
    is_served = is_user_ingbanned(user_id)
    if not is_served:
        ban_db.insert_one({"user_id": user_id, "gban_reason": gban_reason or "None"})
   

def remove_gban(user_id: int):
    is_served = is_user_ingbanned(user_id)
    if is_served:
        ban_db.delete_one({"user_id": user_id})
  

def is_gban(user_id: int) -> bool:
    user = ban_db.find_one({"user_id": user_id, "gban_reason": {"$ne": "None"}})
    if user:
        return True
    return False
def get_gban_list() -> list:
    gban_list = []
    for user in ban_db.find({"gban_reason": {"$ne": "None"}}):
        gban_list.append(user)
    return gban_list
