# src/user.py

import pymongo
from src.database import Database
from time import time
from src import get_config
from random import randint
import bcrypt
from src.session import Session
from mongogettersetter import MongoGetterSetter
from flask import Blueprint, render_template, redirect, url_for, request, session
from uuid import uuid4

db = Database.get_connection()
users = db.users # create a collection users if it doesn't exist

class UserCollection(metaclass=MongoGetterSetter):
    def __init__(self, username):
        self._collection = db.users
        self._filter_query = {
            "$or": [
                {"username": username}, 
                {"id": username}
            ]
        }
        
class User:
    def __init__(self, id):
        self.collection = UserCollection(id)
        self.id = self.collection.id
        self.username = self.collection.username        
    
    @staticmethod
    def login(username, password):
        result = users.find_one({
            "username": username
        })
        if result:
                    
            hashedpw = result['password']
            if bcrypt.checkpw(password.encode(), hashedpw):
                # TODO: Register a session and return a session ID on successful login
                sess = Session.register_session(username, request=request)
                return sess.id
            else:
                raise Exception("Incorrect Password")
        else:
            raise Exception("Incorrect Credentials")

    @staticmethod
    def register(username, password, confirm_password, name, email):
        uuid = str(uuid4())
        existing = users.find_one({"username": username})
        if existing:
            raise Exception("Username already exists")
       
        if password != confirm_password:
            raise Exception("Password and Confirm Password do not match")
        
        password = password.encode()
        salt = bcrypt.gensalt() # like a secret key that is embedded into the password for verification purposes while logging in
        password = bcrypt.hashpw(password, salt)
        _id = users.insert_one({
            "username": username, # TODO: Make as unique index to avoid duplicate entries
            "password": password,
            "register_time": time(),
            "active": False,
            "activate_token": randint(100000, 999999),
            "id": uuid,
            "name": name,
            "email": email
        })
        # we should send this OTP (activate_token) via SMS or Email to the user
        # TODO: Use gmail to send emails with OTP
        return uuid
        
        