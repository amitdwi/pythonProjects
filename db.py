from pymongo import MongoClient
from pymongo.server_api import ServerApi
import urllib
import certifi
import os
from dotenv import load_dotenv

uri = "mongodb+srv://amitdwivedi:"+ urllib.parse.quote("12345") + "@cluster0.0zm9el6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['my_db']