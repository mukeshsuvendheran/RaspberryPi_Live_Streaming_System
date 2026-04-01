import json

class MongoGetterSetter(type):

    """
    `MongoGetterSetter` is a metaclass that provides a convenient getter and setter API for instances of the classes that use it, allowing natural operations in Python objects to easily reflect in MongoDB documents.
    """

    def __call__(cls, *args, **kwargs):
        """
        Return a new instance of the class
        """
        # print(args)
        # print(kwargs)
        instance = super().__call__(*args, **kwargs)
        instance.__class__ = type(
            "PyMongoGetterSetter",
            (cls,), 
            {
                "__getattr__": cls.PyMongoGetterSetter.__getattr__,
                "__getitem__": cls.PyMongoGetterSetter.__getitem__,
                "__setattr__": cls.PyMongoGetterSetter.__setattr__,
                "__setitem__": cls.PyMongoGetterSetter.__setitem__,
                "__contains__": cls.PyMongoGetterSetter.__contains__,
                "__str__": cls.PyMongoGetterSetter.__str__,
                "__repr__": cls.PyMongoGetterSetter.__repr__,
                "__delattr__": cls.PyMongoGetterSetter.__delattr__,
                "__delitem__": cls.PyMongoGetterSetter.__delitem__,
                "delete": cls.PyMongoGetterSetter.delete,
                "set": cls.PyMongoGetterSetter.set,
                "get": cls.PyMongoGetterSetter.get,
                "refresh": cls.PyMongoGetterSetter.refresh,
                "_data": None,
            },
        )
        return instance

    class PyMongoGetterSetter:

        """
        `PyMongoGetterSetter` is a class that provides a convenient getter and setter API for instances of the classes that use it, allowing natural operations in Python objects to easily reflect in MongoDB documents.
        """

        def __getattr__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            if _key in self.__dict__:
                return self.__dict__[_key]
            else:
                data = self._data = self._collection.find_one(self._filter_query) if self._data is None else self._data
                if isinstance(data[_key], dict):
                    dictwrapper = MongoDictWrapper(data[_key])
                    dictwrapper.prepare(
                        data, [_key], self._collection, self._filter_query, self
                    )
                    return dictwrapper
                elif isinstance(data[_key], list):
                    datawrapper = MongoDataWrapper(
                        data, [_key], self._collection, self._filter_query, self
                    )
                    return datawrapper
                else:
                    return data[_key]
                
        def __getitem__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            data = self._data = self._collection.find_one(self._filter_query) if self._data is None else self._data
            if isinstance(data[_key], dict):
                dictwrapper = MongoDictWrapper(data)
                dictwrapper.prepare(
                    data, [_key], self._collection, self._filter_query, self
                )
                return dictwrapper
            elif isinstance(data[_key], list):
                datawrapper = MongoDataWrapper(
                    data, [_key], self._collection, self._filter_query, self
                )
                return datawrapper
            else:
                return data[_key]

        def __setattr__(self, _key, value):
            """
            Set the value of the key in the array/string/object
            """
            if _key in ["_filter_query", "_collection", "_keys", "_data"]:
                self.__dict__[_key] = value
            else:
                _filter_query = self._filter_query
                self._collection.update_one(_filter_query, {"$set": {_key: value}})
                self._data = self._collection.find_one(self._filter_query)

        def __setitem__(self, _key, value):
            """
            Set the value of the key in the array/string/object
            """
            _filter_query = self._filter_query
            self._collection.update_one(_filter_query, {"$set": {_key: value}})
            self._data = self._collection.find_one(self._filter_query)

        def __contains__(self, _key):
            """
            Return the value of the key in the array/string/object
            """
            self._data = self._collection.find_one(self._filter_query) if self._data is None else self._data
            return _key in self._data

        def __str__(self):
            """
            Return the string representation of the array/string/object
            """
            self._data = self._collection.find_one(self._filter_query) if self._data is None else self._data
            return json.dumps(self._data, indent=4, default=str)

        def __repr__(self):
            """
            Return the string representation of the array/string/object
            """
            self._data = self._collection.find_one(self._filter_query) if self._data is None else self._data
            return json.dumps(self._data, indent=4, default=str)

        def __delattr__(self, name):
            """
            Delete the key in the array/string/object using del keyword
            """
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})
            self._data = self._collection.find_one(self._filter_query)

        def __delitem__(self, name):
            """
            Delete the key in the array/string/object using del keyword
            """
            # print(f"___delattr___ name = {name}")
            self._collection.update_one(self._filter_query, {"$unset": {name: ""}})
            self._data = self._collection.find_one(self._filter_query)
            
        def delete(self):
            """
            Delete object from the MongoDB Collection using $unset
            """
            # print(f"deleting {self._id}")
            result = self._collection.delete_one(self._filter_query)
            self._data = None
            return result
            
        
        def __eq__(self, other):
            """
            Return True if the two objects are equal
            """
            return repr(self) == repr(other)
        
        def __ne__(self, other):
            """
            Return True if the two objects are not equal
            """
            return repr(self) != repr(other)
        
        def set(self, data):
            """
            Set the document in the MongoDB Collection
            """
            result = self._collection.update_one(self._filter_query, {"$set": data})
            self._data = self._collection.find_one(self._filter_query)
            return result
            
        def get(self, realtime=False):
            """
            Get the document from the MongoDB Collection
            """
            if realtime or self._data is None:
                self._data = self._collection.find_one(self._filter_query)
            return self._data

        def refresh(self, _data=None):
            """
            Refresh the document from the MongoDB Collection
            """
            if _data is not None:
                self._data = _data
            else:
                self._data = self._collection.find_one(self._filter_query)
                
            return self._data
            

class MongoDataWrapper:

    """
    `MongoDataWrapper` is a subscriptable class, which wraps MongoDB document datatypes to provide MongoDB Array/List Operations over a simple, straightforward API to perform various operations on the MongoDB collection. Check the list of methods for the allowed operations.
    """

    def __init__(self, data, _key, _collection, _filter_query, _context):
        self._data = data
        self._filter_query = _filter_query
        self._collection = _collection
        self._keys = _key
        self._context = _context

    def get(self, _key=None, realtime=False):
        """
        Get the original representation of the document as it exists without MongoGetterSetter Wrappers.
        If no arguments are passed, then return the whole data.
        If _key is passed, it will return the specific value w.r.t the key.
        If realtime is set to true, the data is fetched from MongoDB in realtime

        Args:
            _key (any|None, optional):  Defaults to None.
            realtime (bool, optional): Defaults to False

        Returns:
            any: Original Data without Wrapper

        """
        if realtime:
            self._data = nested_dict = self._collection.find_one(self._filter_query)
            self._context._data = self._data
        else:
            nested_dict = self._context._data

        for k in self._keys:
            nested_dict = nested_dict[k]
        if _key is None:
            return nested_dict
        else:
            return nested_dict[_key]
        
    def refresh(self):
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

    def append(self, *value):
        """
        Append the value to the array. Returns True if the value is appended, else False.
        """

        result = self.push(*value)
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result

    def push(self, *values, maximum=0):
        """
        Push the value to the array. Returns True if the value is pushed, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        if maximum == 0:
            result = self._collection.update_one(
                self._filter_query, {"$push": {path: {"$each": values}}}
            )
            self._data = self._collection.find_one(self._filter_query)
            self._context.refresh(self._data)
            return result.modified_count > 0
        else:
            update_operation = {"$push": {path: {"$each": values, "$slice": -maximum}}}

            result = self._collection.update_one(
                self._filter_query, update_operation
            ).modified_count
            self._data = self._collection.find_one(self._filter_query)
            self._context.refresh(self._data)
            return result.modified_count > 0

    def addToSet(self, value):
        """
        Add the value to the array if it does not exist. Returns True if the value is added, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$addToSet": {path: value}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0

    def pop(self, direction=1):
        """
        Pop the value from the array. Returns True if the value is popped, else False. direction=1 for popping from the end, direction=-1 for popping from the beginning.
        """

        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$pop": {path: direction}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0

    def remove(self, item):
        """
        Remove the value from the array. Returns True if the value is removed, else False.
        """

        result = self.pull(item)
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result

    def count(self):
        """
        Return the length of the array/string/object
        """

        return self.__len__()

    def pull(self, value):
        """
        Remove the value from the array. Returns True if the value is removed, else False.
        """
        
        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$pull": {path: value}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0

    def insert(self, index, value):
        """
        Insert the value at the index in the array. Returns True if the value is inserted, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        insert_query = {"$push": {path: {"$each": [value], "$position": index}}}
        result = self._collection.update_one(self._filter_query, insert_query)
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0
        
    def index(self, value):
        """
        Find the index of the value in array. If the value is not present, you will get -1.
        """
        path = ".".join(str(v) for v in self._keys)
        # print(path)
        pipeline = [
            {
                "$match": self._filter_query,
            },
            {
                "$project": {
                    "index": { "$indexOfArray": [path, value] }
                }
            }
        ]
        #print(pipeline)
        result = list(self._collection.aggregate(pipeline))
        return result[0]["index"]


    def pullAll(self, *values):
        """
        Remove all the (given) values from the array. Returns True if the value is removed, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$pullAll": {path: values}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0

    def matchSize(self, value):
        """
        Check if the array has the given size. Returns True if the array has the given size, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$size": value}}))

    def elemMatch(self, **kvalues):
        """
        Check if the array has an element that matches the given key-value pairs. Returns True if the array has an element that matches the given key-value pairs, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$elemMatch": kvalues}}))

    def matchAll(self, *values):
        """
        Check if the array has all the given values. Returns True if the array has all the given values, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        return bool(self._collection.find_one({path: {"$all": values}}))

    def update(self, field, match, **kvalues):
        """
        Update the value of the field in the array element that matches the given value. Returns True if the value is updated, else False.
        """

        path = ".".join(str(v) for v in self._keys)
        _filter_query = dict(self._filter_query)
        update_query = {
            path + f".$[elem]." + _key: value for _key, value in kvalues.items()
        }
        _filter_query[path + "." + field] = match
        result = self._collection.update_one(
            self._filter_query,
            {"$set": update_query},
            array_filters=[{f"elem.{field}": match}],
            upsert=True,
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result.modified_count > 0

    def __len__(self):
        """
        Return the length of the array/string/object
        """

        return len(self.get())

    def __str__(self):
        """
        Return the string representation of the array/string/object
        """

        # nested_dict = self._data
        # for k in self._keys:
        #     nested_dict = nested_dict[k]
        return json.dumps(self.get(), indent=4, default=str)

    def __repr__(self):
        """
        Return the string representation of the array/string/object
        """

        # nested_dict = self._data
        # for k in self._keys:
        #     nested_dict = nested_dict[k]
        return json.dumps(self.get(), indent=4, default=str)

    def __getitem__(self, _key):
        """
        Return the value of the key in the array/string/object
        """

        data = self.get(_key)
        # return data[_key]
        if isinstance(data, dict):
            dictwrapper = MongoDictWrapper(data)
            dictwrapper.prepare(
                self._data, self._keys + [_key], self._collection, self._filter_query, self._context
            )
            return dictwrapper
        elif isinstance(data, list):
            datawrapper = MongoDataWrapper(
                self._data, self._keys + [_key], self._collection, self._filter_query, self._context
            )
            return datawrapper
        else:
            return data
            
    def __getattr__(self, _key):
        """
        Return the value of the key in the array/string/object
        """

        if _key in self.__dict__:
            return self.__dict__[_key]
        else:
            data = self.get(_key)
            # return data[_key]
            if isinstance(data, dict):
                dictwrapper = MongoDictWrapper(data)
                dictwrapper.prepare(
                    self._data, self._keys + [_key], self._collection, self._filter_query, self._context
                )
                return dictwrapper
            elif isinstance(data, list):
                datawrapper = MongoDataWrapper(
                    self._data, self._keys + [_key], self._collection, self._filter_query, self._context
                )
                return datawrapper
            else:
                return data
                
    def __setattr__(self, _key, value):
        """
        Set the value of the key in the array/string/object
        """
        _key = str(_key)
        if _key in ["_filter_query", "_collection", "_keys", "_data", "_context"]:
            self.__dict__[_key] = value
        else:
            path = ".".join(str(v) for v in self._keys)
            self._collection.update_one(
                self._filter_query, {"$set": {path + "." + _key: value}}
            )
            self._data = self._collection.find_one(self._filter_query)
            self._context.refresh(self._data)

    def __setitem__(self, index, value):
        """
        Set the value of the key in the array/string/object
        """
        path = ".".join(str(v) for v in self._keys)
        update_query = {path + "." + str(index): value}
        self._collection.update_one(self._filter_query, {"$set": update_query})
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

    def __delitem__(self, _key):
        """
        Delete the key in the array/string/object using del keyword
        """
        path = ".".join(str(v) for v in self._keys)
        data = self.get()
        _key = str(_key)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        if isinstance(data, list):
            self.pull(None)
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

    def __delattr__(self, _key):
        """
        Delete the key in the array/string/object using del keyword
        """
        path = ".".join(str(v) for v in self._keys + [_key])
        data = self.get()
        _key = str(_key)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        if isinstance(data, list):
            self.pull(None)
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
    
    def __contains__(self, _key):
        return _key in self.get()

    def delete(self):
        """
        Delete the nested object from the MongoDB Document using $unset
        """
        
        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$unset": {path: ""}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result
    
    def refresh(self):
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

class MongoDictWrapper(dict):
    """
    MongoDictWrapper is a wrapper around the dictionary object to provide the functionality of updating the database when the dictionary is updated. It is used to wrap the dictionary object in the MongoGetterSetter class. It is not meant to be used directly.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def refresh(self):
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

    def prepare(self, _data, _keys, _collection, _filter_query, _context):
        """
        Prepare the MongoDictWrapper object to be used. This method is called by the MongoGetterSetter class when the object is created.
        """
        self._data = _data
        self._filter_query = _filter_query
        self._collection = _collection
        self._keys = _keys
        self._context = _context
        # path = '.'.join(str(v) for v in self._keys)
        # print(f"__prepare__ you are at: {path}")

    def __setattr__(self, _key, value):
        _key = str(_key)
        """
        Set the value of the key in the dictionary and update the database.
        """
        if _key in ["_filter_query", "_collection", "_keys", "_data", "_context"]:
            self.__dict__[_key] = value
        else:
            # Call the parent __setitem__ method to actually set the value in the dictionary
            path = ".".join(str(v) for v in self._keys)
            # Execute your function here
            # # print(f"Dictionary updated: {path}.{_key}={value}")
            update = {"$set": {"{}.{}".format(path, _key): value}}
            result = self._collection.update_one(self._filter_query, update)
            self._data = nested_dict = self._collection.find_one(self._filter_query)
            for k in self._keys:
                nested_dict = nested_dict[k]
            # print(f"__setitem__ {str(nested_dict)}")
            super().update(nested_dict)
            self._context.refresh(self._data)
        

    def __getattr__(self, _key):
        """
        Get the value of the key in the dictionary. 
        All dict will be wrapped with MongoDictWrapper.
        All list will be wrapped with MongoDataWrapper.
        """
        
        _key = str(_key)
        if _key in self.__dict__:
            return self.__dict__[_key]
        else:
            path = ".".join(str(v) for v in self._keys)
            # print(f"__getitem__ you are at: {path}")
            original_dict = self._context._data
            nested_dict = dict(original_dict)
            for k in self._keys:
                nested_dict = nested_dict[k]
            super().update(nested_dict)
            # print(f"__getitem__ {str(nested_dict)}")
            if isinstance(nested_dict[_key], dict):
                dictwrapper = MongoDictWrapper(nested_dict[_key])
                dictwrapper.prepare(
                    original_dict, self._keys + [_key], self._collection, self._filter_query, self._context
                )
                return dictwrapper
            elif isinstance(nested_dict[_key], list):
                datawrapper = MongoDataWrapper(
                    original_dict, self._keys + [_key], self._collection, self._filter_query, self._context
                )
                return datawrapper
            else:
                return nested_dict[_key]

    def __getitem__(self, _key):
        _key = str(_key)
        """
        Get the value of the key in the dictionary. 
        All dict will be wrapped with MongoDictWrapper.
        All list will be wrapped with MongoDataWrapper.
        """
        path = ".".join(str(v) for v in self._keys)
        # print(f"__getitem__ you are at: {path}")
        original_dict = self._context._data
        nested_dict = dict(original_dict)
        for k in self._keys:
            nested_dict = nested_dict[k]
        super().update(nested_dict)
        # print(f"__getitem__ {str(nested_dict)}")
        if isinstance(nested_dict[_key], dict):
            dictwrapper = MongoDictWrapper(nested_dict[_key])
            dictwrapper.prepare(
                original_dict, self._keys + [_key], self._collection, self._filter_query, self._context
            )
            return dictwrapper
        elif isinstance(nested_dict[_key], list):
            datawrapper = MongoDataWrapper(
                original_dict, self._keys + [_key], self._collection, self._filter_query, self._context
            )
            return datawrapper
        else:
            return nested_dict[_key]

    def __setitem__(self, _key, value):
        _key = str(_key)
        """
        Set the value of the key in the dictionary and update the database.
        """
        # Call the parent __setitem__ method to actually set the value in the dictionary
        path = ".".join(str(v) for v in self._keys)
        # Execute your function here
        # # print(f"Dictionary updated: {path}.{_key}={value}")
        update = {"$set": {"{}.{}".format(path, _key): value}}
        result = self._collection.update_one(self._filter_query, update)
        self._data = nested_dict = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        for k in self._keys:
            nested_dict = nested_dict[k]
        # print(f"__setitem__ {str(nested_dict)}")
        super().update(nested_dict)

    def __delitem__(self, _key):
        _key = str(_key)
        """
        Delete the item from the dictionary and update the database.
        """
        super().__delitem__(_key)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)

    def __delattr__(self, _key):
        _key = str(_key)
        """
        Delete the item from the dictionary and update the database.
        """
        super().__delitem__(_key)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
    
    def delete(self):
        """
        Delete the nested object from the MongoDB Document using $unset
        """
        
        path = ".".join(str(v) for v in self._keys)
        result = self._collection.update_one(
            self._filter_query, {"$unset": {path: ""}}
        )
        self._data = self._collection.find_one(self._filter_query)
        self._context.refresh(self._data)
        return result

    def get(self, _key=None, default=None, realtime=False):
        """
        Get the value of the key from the dictionary. 
        If the key is not present, the function will return the whole dict. 
        If key is passed and is not None and is present in dict, the appropriate value for the key will be returned.
        If key is passed and is not present in the dict, default value will be returned.
        """
        if realtime:
            self._data = self._collection.find_one(self._filter_query)
            original_dict = self._data
            self._context.refresh(self._data)
            nested_dict = dict(original_dict)
            for k in self._keys:
                nested_dict = nested_dict[k]
            data = nested_dict
        else:
            nested_dict = self._context._data
            for k in self._keys:
                nested_dict = nested_dict[k]
            data = nested_dict
            # data = dict(self)


        if _key is None:
            return dict(data)
        if _key in self:
            return self[_key]
        else:
            return default

    def pop(self, _key, default=None):
        """
        Pop the value of the key from the dictionary and update the database. If the key is not present, return the default value.
        """
        value = super().pop(_key, default)
        path = ".".join(str(v) for v in self._keys)
        self._collection.update_one(
            self._filter_query, {"$unset": {path + "." + _key: ""}}
        )
        self._context.refresh()
        return value

    def update(self, other):
        """
        Update the dictionary with the other dictionary and update the database.
        """

        super().update(other)
        d = dict(self)
        other.update(d)
        path = ".".join(str(v) for v in self._keys)
        update = {"$set": {path: other}}
        result = self._collection.update_one(self._filter_query, update, upsert=True)
        self._context.refresh()
        return result

    def clear(self):
        """
        Clear the dictionary and update the database.
        """

        # print("__clear__ ")
        path = ".".join(str(v) for v in self._keys)
        update = {"$set": {path: {}}}
        result = self._collection.update_one(self._filter_query, update)
        super().clear()
        self._context.refresh()
        return result

