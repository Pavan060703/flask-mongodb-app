from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from urllib.parse import quote_plus
import os

app = Flask(__name__)

def build_mongo_uri():
    uri = os.environ.get("MONGODB_URI")
    if uri:
        return uri
    user = os.environ.get("MONGO_USERNAME")
    password = os.environ.get("MONGO_PASSWORD")
    host = os.environ.get("MONGO_HOST", "localhost")
    port = os.environ.get("MONGO_PORT", "27017")
    if user and password:
        return (f"mongodb://{quote_plus(user)}:{quote_plus(password)}"
                f"@{host}:{port}/?authSource=admin")
    return f"mongodb://{host}:{port}/"

client = MongoClient(build_mongo_uri(), serverSelectionTimeoutMS=5000)
db = client.flask_db
collection = db.data

@app.route('/')
def index():
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"

@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        data = request.get_json()
        collection.insert_one(data)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        data = list(collection.find({}, {"_id": 0}))
        return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
