from MukeshRobot import MONGO_DB_URI
from pymongo import MongoClient

myclient = MongoClient(MONGO_DB_URI)
chat=myclient["MUK_chats"]
chatsdb= chat["MUK_chats"]

def get_served_chats() -> list:
    chats_list = []
    for user in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(user)
    return chats_list

def is_served_chat(chat_id: int) -> bool:
    chat = chatsdb.find_one({"chat_id": chat_id})
    return chat is not None

def add_served_chat(chat_id: int):
    if is_served_chat(chat_id):
        return
    chatsdb.insert_one({"chat_id": chat_id})

def remove_served_chat(chat_id: int):
    if not is_served_chat(chat_id):
        return
    chatsdb.delete_one({"chat_id": chat_id})
