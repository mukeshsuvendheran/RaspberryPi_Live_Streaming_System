#device
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config
from services.device_api_services import API
from db.database import Database
from utils import MongoGetterSetter
from uuid import uuid4
import time

db = Database.get_connection()

class DeviceCollection(metaclass=MongoGetterSetter):
    def __init__(self, id):
        self._collection = db.devices
        self._filter_query = {
            '$or': [
                {'id': id},
            ]
        }
        
class Device:
    def __init__(self, id):
        self.collection = DeviceCollection(id)
        self.id = self.collection.id
    
    def delete(self):
        api = API(self.collection.api)
        api.collection.linked_device = None #unlink the device from API
        self.collection.delete()
        
    @staticmethod
    def register_device(name, username, _type, api_key, remarks):
        uuid = str(uuid4())
        
        #Link the device to API
        api = API(api_key)
        api.collection.linked_device = uuid
        
        collection = db.devices
        result = collection.insert_one({
            "id": uuid,
            "user": username,
            "name": name,
            "remarks": remarks,
            "group": api.collection.group,
            "type": _type,
            "active": True,
            "registered_on": time(),
            "api": api_key,
            "last_seen": None,
            "created_at": datetime.utcnow()
        })
        
        return Device(uuid)
    
    @staticmethod
    def get_devices():
        collection = db.devices
        return collection.find({})
        
        