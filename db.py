from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi
import os
from dotenv import load_dotenv

load_dotenv('.env')

uri=os.getenv('MONGO_URI')
client=MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db=client['my_db']