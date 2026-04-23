#device API Key Management
from flask import Blueprint, render_template, redirect, url_for, request, session
from models.help import get_config
from db.database import Database
from utils import MongoGetterSetter
from uuid import uuid4
import time
from models.help import md5_hash

db = Database.get_connection()

class APICollection(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._collection = db.api_keys
        self._filter_query = {'$or': [ 
            {'id': _id},
            {'hash': _id}
        ]}
        
class API:
    def __init__(self, _id):
        self.collection = APICollection(_id)
        try:
            self.id = str(self.collection.id)
        except TypeError:
            raise Exception("API Key not found")
        
    def get_device(self):
        device = db.devices.find_one({"api": self.collection.hash})
        try:
         return device
        except TypeError:
            raise Exception("Device not found")
    
        
    def is_valid(self):
        login_time = self.collection.time
        validity = self.collection.validity
        if validity == 0:
            return self.collection.active # means its valid forever
        else:
            if self.collection.active:
                now = time()
                return now - login_time < validity
            else:
                return False
    
    def delete(self):
        self.collection.delete()
        
    @staticmethod
    def get_all_keys(session, only_unlinked=False):
        if not session.get('authenticated') or not session.get('username'):
            raise Exception("User not authenticated")
        
        collection = db.api_keys
        username = session.get('username')
        if only_unlinked:
            query = {"username": username, "linked_device": None}
        else:
            query = {"username": username}
        result = collection.find(query)
        return result
        
    @staticmethod
    def register_api_key(session, name, group, remarks, request=None, validity=0, _type="api"):
        if not session.get('authenticated') or not session.get('username'):
            raise Exception("User not authenticated")
        
        uuid = str(uuid4())
        collection = db.api_keys
        username = session.get('username')
        if request is not None:
            request_info = {
                'ip': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'method': request.method,
                'url': request.url,
                # 'headers': dict(request.headers),
                # 'data': request.get_data().decode('utf-8')
            }
        else:
            request_info = None
        
        DEVICE_API_KEY_INFO = collection.insert_one({
            "id": uuid,
            "hash": md5_hash(uuid),
            "username": username,
            "name": name, #device name or key name
            "group": group,
            "remarks": remarks,
            "time": time(),
            "validity": validity, # 7 days,
            "active": True,
            "type": _type, 
            "request": request_info,
            "linked_device": None
        })
        
        return API(uuid)
        
        



# # api_key_management.py

# import hashlib
# import time
# from uuid import uuid4
# from functools import wraps

# from src.database import Database

# db = Database.get_connection()

# # =========================
# # 🔐 HASHING (SECURE)
# # =========================
# def sha256_hash(value: str) -> str:
#     return hashlib.sha256(value.encode()).hexdigest()


# # =========================
# # 🚫 RATE LIMITING (simple)
# # =========================
# RATE_LIMIT = 60  # requests
# RATE_WINDOW = 60  # seconds

# rate_cache = {}  # {api_hash: [timestamps]}

# def rate_limiter(func):
#     @wraps(func)
#     def wrapper(self, *args, **kwargs):
#         api_hash = self.collection["hash"]
#         now = time.time()

#         if api_hash not in rate_cache:
#             rate_cache[api_hash] = []

#         # remove old timestamps
#         rate_cache[api_hash] = [
#             t for t in rate_cache[api_hash]
#             if now - t < RATE_WINDOW
#         ]

#         if len(rate_cache[api_hash]) >= RATE_LIMIT:
#             raise Exception("Rate limit exceeded")

#         rate_cache[api_hash].append(now)

#         return func(self, *args, **kwargs)

#     return wrapper


# # =========================
# # 📦 API CLASS
# # =========================
# class API:
#     def __init__(self, key: str):
#         self.raw_key = key
#         self.hash = sha256_hash(key)

#         self.collection = db.api_keys.find_one({"hash": self.hash})

#         if not self.collection:
#             raise Exception("Invalid API Key")

#     # =========================
#     # ✅ VALIDATION
#     # =========================
#     def is_valid(self):
#         if not self.collection["active"]:
#             return False

#         validity = self.collection["validity"]
#         created_time = self.collection["time"]

#         if validity == 0:
#             return True

#         return (time.time() - created_time) < validity

#     # =========================
#     # 🔐 SCOPE CHECK
#     # =========================
#     def has_scope(self, required_scope):
#         scopes = self.collection.get("scope", [])
#         return required_scope in scopes

#     # =========================
#     # 🔗 DEVICE BINDING
#     # =========================
#     def get_device(self, device_id=None):
#         device = db.devices.find_one({"api": self.hash})

#         if not device:
#             if device_id:
#                 # first-time binding
#                 db.devices.update_one(
#                     {"id": device_id},
#                     {"$set": {"api": self.hash}}
#                 )
#                 return db.devices.find_one({"id": device_id})
#             else:
#                 raise Exception("Device not linked")

#         return device

#     # =========================
#     # 📊 USAGE TRACKING
#     # =========================
#     def update_usage(self):
#         db.api_keys.update_one(
#             {"hash": self.hash},
#             {
#                 "$inc": {"usage_count": 1},
#                 "$set": {"last_used": time.time()}
#             }
#         )

#     # =========================
#     # 📜 LOGGING
#     # =========================
#     def log_request(self, request=None):
#         if not request:
#             return

#         log = {
#             "api_hash": self.hash,
#             "time": time.time(),
#             "ip": request.remote_addr,
#             "endpoint": request.path,
#             "method": request.method
#         }

#         db.api_logs.insert_one(log)

#     # =========================
#     # 🔥 MAIN VALIDATED ACCESS
#     # =========================
#     @rate_limiter
#     def authorize(self, scope=None, device_id=None, request=None):
#         if not self.is_valid():
#             raise Exception("API Key expired or inactive")

#         if scope and not self.has_scope(scope):
#             raise Exception("Permission denied")

#         device = self.get_device(device_id=device_id)

#         self.update_usage()
#         self.log_request(request)

#         return device

#     # =========================
#     # ❌ DELETE KEY
#     # =========================
#     def delete(self):
#         db.api_keys.delete_one({"hash": self.hash})

#     # =========================
#     # 📥 GET USER KEYS
#     # =========================
#     @staticmethod
#     def get_all_keys(session):
#         if not session.get("authenticated"):
#             raise Exception("Unauthorized")

#         return db.api_keys.find({
#             "username": session["username"]
#         })

#     # =========================
#     # 🆕 CREATE API KEY
#     # =========================
#     @staticmethod
#     def create_key(session, name, scope=None, validity=0, remarks=""):
#         if not session.get("authenticated"):
#             raise Exception("Unauthorized")

#         raw_key = f"iot_live_{uuid4().hex}"
#         hashed = sha256_hash(raw_key)

#         db.api_keys.insert_one({
#             "hash": hashed,
#             "username": session["username"],
#             "name": name,
#             "scope": scope or ["read"],
#             "remarks": remarks,
#             "time": time.time(),
#             "validity": validity,
#             "active": True,
#             "linked_device": None,
#             "usage_count": 0,
#             "last_used": None
#         })

#         # ⚠️ RETURN RAW KEY ONLY ONCE
#         return raw_key