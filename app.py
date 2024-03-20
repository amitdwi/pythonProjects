from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from json import JSONEncoder
from bson import json_util
import urllib
import certifi

app = Flask(__name__)

uri = "mongodb+srv://amitdwivedi:"+ urllib.parse.quote("Welcome@123") + "@cluster0.0zm9el6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['my_db']
collection = db['users']

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        return json_util.default(obj)

app.json_encoder = CustomJSONEncoder

@app.route('/')

def home():
    return 'Welcome to Home page'

@app.route('/users/<int:user_id>', methods=['GET'])

def get_user(user_id):
    user = collection.find_one({"id": user_id})
    
    return json_util.dumps(user), 200

@app.route('/users', methods=['POST'])

def create_user():
    data = request.get_json()
    collection.insert_one({"id": data['id'], "name": data['name'], "age": data['age']})
    return jsonify({"message": "User added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
    