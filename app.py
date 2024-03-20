from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
#from json import JSONEncoder
#from bson import json_util
import urllib
import certifi
import bcrypt

app = Flask(__name__)

uri = "mongodb+srv://amitdwivedi:"+ urllib.parse.quote("12345") + "@cluster0.0zm9el6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['my_db']
collection = db['users']

user_schema = {
    'email': str,
    'password': str
}

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


@app.route('/')
def home():
    return 'Welcome to Home page'


@app.route('/register', methods=['POST'])
def user_register():
    user_data = request.json
    new_user = {key: user_data[key] for key in user_schema.keys()}
    new_user['password'] = hash_password(new_user['password'])
    result = collection.insert_one(new_user)
    return jsonify({'message': 'User registered successfully'}), 201


if __name__ == "__main__":
    app.run(debug=True)
    