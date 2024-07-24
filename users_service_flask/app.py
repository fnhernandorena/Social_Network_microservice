from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId   
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = MongoClient("MONGO_URI")
db = client['microservices']
users_collection = db['users']

class User:
    def __init__(self, username: str, age: int, email: str):
        self.username = username
        self.age = age
        self.email = email

    def to_dict(self):
        return {
            "username": self.username,
            "age": self.age,
            "email": self.email
        }

def serialize_user(user):
    """Convert MongoDB user document to JSON serializable format"""
    user["_id"] = str(user["_id"])
    return user

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        return jsonify({"error": "Invalid user ID format"}), 400

    if user:
        response = requests.get(f"http://localhost:5001/api/posts/{user_id}")
        posts = response.json() if response.status_code == 200 else []
        user['posts'] = posts
        return jsonify(serialize_user(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "age", "email")):
        return jsonify({"error": "Invalid data"}), 400

    user = User(username=data['username'], age=data['age'], email=data['email'])
    user_dict = user.to_dict()

    result = users_collection.insert_one(user_dict)
    if result.inserted_id:
        return jsonify({"message": "User created", "user_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"error": "Failed to create user"}), 500

@app.route('/api/allusers', methods=['GET'])
def get_all_users():
    users = users_collection.find()
    users_list = [serialize_user(user) for user in users]
    return jsonify(users_list), 200


if __name__ == '__main__':
    app.run(debug=True)
