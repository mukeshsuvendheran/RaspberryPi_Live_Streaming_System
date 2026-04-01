from src import get_config
from src.User import User
from src.Database import Database
from src.Group import Group, GroupCollection
from src.API import API, APICollection

from pymongo import MongoClient
from mongogettersetter import MongoGetterSetter

# Connect to the MongoDB database and collection

client = Database.get_connection()
collection = client["employees"]

# Wrapper for MongoDB Collection with metaclass, use this inside your actual class.
class EmployeeCollection(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._filter_query = {"id": _id} # or the ObjectID, at your convinence
        self._collection = collection # Should be a pymongo.MongoClient[database].collection

class Employee:
    def __init__(self, _id):
        self._filter_query = {"id": _id}
        self._collection = collection
        self.collection = EmployeeCollection(_id)

        # Create a new document if it doesn't exist
        if self.collection.get() is None:
            self._collection.insert_one(self._filter_query)
    
    def someOtherOperation(self):
        self.collection.hello = "Hello World"  

e = EmployeeCollection(4051)
print(e.get())

# # g = Group.register_group("Test Group", "This is a test group")
# # print(g.id)

# g = Group('asdasd')
# print(g.collection.id)

# a = API("93c01867-989e-4be4-ba38-c574390065b0")
# print(a.is_valid())
# coll = a.collection
# coll.something = "askjdfn aksjdn"
# coll.something1 = "asdlnadlkand"
# coll.asdlknasd = "asldkjnqadkljnasld"
# coll.set({
#     "something": "askjdfn aksjdn"
#     "something1": "asdlnadlkand"
#     "asdlknasd": "asldkjnqadkljnasld"
# })
# a = API.register_api_key("Test", "skjnakjsd", "asdhkasdhbasjhd")
# print(a.collection.id)