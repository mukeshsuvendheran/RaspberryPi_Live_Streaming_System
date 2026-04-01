from src.Database import Database
from mongogettersetter import MongoGetterSetter


class EmployeeCollection(metaclass=MongoGetterSetter):
    def __init__(self, _id):
        self._filter_query = {"id": _id}
        self._collection = Database.get_connection().employees
    

class Employee():
    def __init__(self, _id):
        self.collection = EmployeeCollection(_id)
        self._filter_query = {"id": _id}
        self._collection = Database.get_connection().employees
        
        if self.collection.get() is None:
            self._collection.insert_one(self._filter_query)
        
    def addInfo(self, username):
        if "additional_usernames" in self.collection:
            self.collection.additional_usernames.push(username)
        else:
            self.collection.additional_usernames = []
            self.collection.additional_usernames.push(username)

    def otherFunc(self, newname):
        self.collection.name = newname
        
            
    def lenInfo(self):
        return len(self.collection.additional_usernames)

e = Employee(40599)
e.collection.projects = [
    {
        "title": "Project A",
        "status": "completed"
    },
    {
        "title": "Project B",
        "status": "in progress"
    }
]


m = e.collection
