from mongogettersetter import MongoGetterSetter
from src.database import Database
from uuid import uuid4
from time import time
from src.API import API

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
    
    def delete():
        api = API(self.collection.api)
        api.collection.linked_device = None
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
        })
        
        return Device(uuid)
    
    @staticmethod
    def get_devices():
        collection = db.devices
        return collection.find({})
        
        