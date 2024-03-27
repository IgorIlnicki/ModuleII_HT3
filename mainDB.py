from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://us:us1@cluster0.g6s22by.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.quot
# Send a ping to confirm a successful connection
try:
    # Вставлення даних у колекцію 'qoutes'
    db.qoutes.insert_one({"name": 'Barsik', "age": 3, "features": "FFF"})
    # Вставлення даних у колекцію 'authors'
    db.authors.insert_one({"fullname": dat0, "born_date": dat1, "born_location": dat2, "description": dat3})
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)