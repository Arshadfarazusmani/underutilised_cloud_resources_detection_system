# db.py
# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from bson.objectid import ObjectId

# load_dotenv()

# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise ValueError("MONGO_URI not found in .env")

# client = MongoClient(MONGO_URI)
# db = client["idle_detection_db"]

# users_col = db["users"]
# resources_col = db["resources"]
# predictions_col = db["predictions"]

# # helper: convert ObjectId to string (for returned docs)
# def oid_to_str(doc):
#     if not doc:
#         return None
#     doc["_id"] = str(doc["_id"])
#     return doc

# # add user
# def insert_user(doc):
#     res = users_col.insert_one(doc)
#     return str(res.inserted_id)

# def find_user_by_email(email):
#     return users_col.find_one({"email": email})

# def find_user_public_by_email(email):
#     user = users_col.find_one({"email": email}, {"password": 0})
#     return oid_to_str(user)

# def insert_resource(doc):
#     res = resources_col.insert_one(doc)
#     return str(res.inserted_id)

# def insert_prediction(doc):
#     res = predictions_col.insert_one(doc)
#     return str(res.inserted_id)

# def find_predictions_by_user_email(email, limit=200):
#     cursor = predictions_col.find({"user_email": email}).sort("_id", -1).limit(limit)
#     result = []
#     for p in cursor:
#         p["_id"] = str(p["_id"])
#         result.append(p)
#     return result


# db.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env")

client = MongoClient(MONGO_URI)
db = client["idle_detection_db"]

users_col = db["users"]
resources_col = db["resources"]
predictions_col = db["predictions"]

# helper: convert ObjectId to string (for returned docs)
def oid_to_str(doc):
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc

# add user
def insert_user(doc):
    res = users_col.insert_one(doc)
    return str(res.inserted_id)

def find_user_by_email(email):
    return users_col.find_one({"email": email})

def find_user_public_by_email(email):
    user = users_col.find_one({"email": email}, {"password": 0})
    return oid_to_str(user)

def insert_resource(doc):
    res = resources_col.insert_one(doc)
    return str(res.inserted_id)

def insert_prediction(doc):
    res = predictions_col.insert_one(doc)
    return str(res.inserted_id)

def find_predictions_by_user_email(email, limit=200):
    cursor = predictions_col.find({"user_email": email}).sort("_id", -1).limit(limit)
    result = []
    for p in cursor:
        p["_id"] = str(p["_id"])
        result.append(p)
    return result
