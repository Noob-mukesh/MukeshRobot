from MukeshRobot import MONGO_DB_URI
from pymongo import MongoClient

myclient = MongoClient(MONGO_DB_URI)

users =myclient["MUK_users"]
usersdb = users["MUK_users"]

ban_db=users["gban_db"]



def is_served_user(user_id: int) -> bool:
    user = usersdb.find_one({"user_id": user_id})
    if user is not None:  # Check if the user is not None before using await
        return True
    return False

def get_served_users() -> list:
    users_list = []
    for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

def save_id(user_id: int):
    is_served = is_served_user(user_id)
    if is_served:
        return
    usersdb.insert_one({"user_id": user_id})

def remove_served_users(user_id: int):
    is_served = is_served_user(user_id)
    if not is_served:
        return
    usersdb.delete_one({"user_id": user_id})
    
    
