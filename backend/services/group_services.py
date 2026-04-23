from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config
from db.database import Database
from utils import MongoGetterSetter
from uuid import uuid4
from time import time

db = Database.get_connection()

class GroupCollection(metaclass=MongoGetterSetter):
    def __init__(self, id):
        self._collection = db.groups
        self._filter_query = {
            '$or': [
                {'id': id},
                {'name': id}
            ]
        }
        
class Group:
    def __init__(self, id):
        self.collection = GroupCollection(id)
        self.id = self.collection.id
        
    @staticmethod
    def register_group(name, description):
        uuid = str(uuid4())
        collection = db.groups
        result = collection.insert_one({
            "id": uuid,
            "name": name,
            "description": description,
            "active": True,
        })
        
        return Group(uuid)
    
    @staticmethod
    def get_groups():
        collection = db.groups
        return collection.find({})
        
        