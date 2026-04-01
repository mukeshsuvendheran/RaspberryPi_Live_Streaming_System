import pymongo
from src.Database import Database
from time import time
from src import get_config
from random import randint
import bcrypt

db = Database.get_connection()
users = db.users # create a collection users if it doesn't exist

class User:
    def __init__(self, id):
        print("Init user with {}".format(id))
        # TODO: Build a user object if user is available
        
    
    @staticmethod
    def login(username, password):
        result = users.find_one({
            "username": username
        })
        if result:
            # # this is very veyr insecure
            # # alternate: if result.get('password') == password:
            # if result['password'] == password:
            #     # TODO: initialize session token for additional security
            #     return True
            # else:
            #     raise Exception("Incorrect Password")
            
            hashedpw = result['password']
            if bcrypt.checkpw(password.encode(), hashedpw):
                # TODO: Register a session and return a session ID on successful login
                return True
            else:
                raise Exception("Incorrect Password")
        else:
            raise Exception("Incorrect Credentials")
        

    @staticmethod
    def register(username, password, confirm_password):
        # TODO: Avoid duplicate signups
        if password != confirm_password:
            raise Exception("Password and Confirm Password do not match")
        
        password = password.encode()
        salt = bcrypt.gensalt() # like a secret key that is embedded into the password for verification purposes while logging in
        password = bcrypt.hashpw(password, salt)
        id = users.insert_one({
            "username": username, # TODO: Make as unique index to avoid duplicate entries
            "password": password,
            "register_time": time(),
            "active": False,
            "activate_token": randint(100000, 999999)           
        })
        
        # we should send this OTP (activate_token) via SMS or Email to the user
        # TODO: Use gmail to send emails with OTP
        
        return id
        
        