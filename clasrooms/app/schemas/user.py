from flask import Flask,jsonify,request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://vardges:password1234@cluster0.8yb8n.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_db']
user_collection = db['users']

@app.route('/user',methods=['POST'])
def create_user():
    data = request.get_json()
    if 'name' not in data or 'emai' not in data:
        return jsonify({"error":"email and name are required"})
    
    user = {}
    result = user_collection.insert_one(user)
    user['id'] = str(result.inserted_id)
    return jsonify(user),201

@app.route('/users',methods=['GET'])
def get_users():
    users = []
    for user in user_collection.find():
        user['_id'] = str(user['_id'])
        users.append(user)
    return jsonify(users),200

@app.route('/users/<user_id>',methods=['GET'])
def get_user_by_id(user_id):
    user = user_collection.find_one({'_id':ObjectId(user_id)})
    if user:
        user['_id']=str(user['_id'])
        return jsonify(user,200)
    else:
        return jsonify({'error':"user not foun"}),404
    
@app.route('/user/<user_id>',methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = user_collection.find_one({"_id":ObjectId(user_id)})
    if not user:
        return jsonify({"error":"user not found"}),404
    
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'email' in data:
        update_data['email'] = data['email']
    if 'surname' in data:
        update_data['surname'] = data['surname']
    
    user_collection.update_one({"_id":object(user_id)},{"$set":update_data})
    user = user_collection.find_one({"_id":ObjectId(user_id)})
    user['_id'] = str(user['_id'])
    return jsonify(user), 200

@app.route('/user/<user_id>',methods=['DELETE'])
def delete_user(user_id):
    result = user_collection.delete_one({'_id':ObjectId(user_id)})
    if result.deleted_count>0:
        return jsonify({"message":"user deleted successfully"}), 200
    else:
        return jsonify({"error":"user not found"}), 404
    