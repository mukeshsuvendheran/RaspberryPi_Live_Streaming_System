from pymongo import MongoClient

client = MongoClient('mongodb://sibidharan:gYhsut-6gotzu-mafxov@mongodb.selfmade.ninja:27017/?authSource=users')

db = client.sibidharan_iotcloud 
# db = client['sibidharan_iotcloud'] alternate way

result = db.test.find_one({
    "username": "sibidharan"
})

print(result)
