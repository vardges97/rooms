from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client['rooms_db']
room_collection = db['rooms']

@app.route('/rooms',methods = ['POST'])
def create_room():
    data = request.get_json
    room = {"type":data["type"],
            "name":["name"],
            "capacity":["capacity"],
            "equipement":["equipment"],
            "availability": ["availability"]}
    result = room_collection.insert_one(room)
    room["_id"] = str(result.inserted_id)
    return jsonify(room), 201

@app.route('/rooms',methods = ['GET'])
def get_rooms():
    rooms = []
    for room in room_collection.find():
        room['_id'] = str(room['_id'])
        rooms.append(room)
    return jsonify(rooms), 201

@app.route('/rooms/<room_id>',methods=['get'])
def get_room_by_id(room_id):
    room = room_collection.find_one({"_id":ObjectId(room_id)})
    if room:
        room["id"] = str(room['_id'])
        return jsonify(room), 200
    else:
        return jsonify({"error":"room not found"}),404
    
@app.route('/rooms/<room_id>',methods=['PUT'])
def update_room(room_id):
    data = request.get_json()
    room = room_collection.find_one({"_id":ObjectId(room_id)})
    if not room:
        return jsonify({"error":"room not found"}),404
    
    update_data = {}
    if 'name' in data:
        update_data['name'] = data['name']
    if 'cpascity' in data:
        update_data['cpacity'] = data['cpacity']
    if 'equipement' in data:
        update_data['equipement'] = data['equipement']
    if 'availability' in data:
        update_data['availability'] = data['availability']
    
    room_collection.update_one({"_id":ObjectId(room_id)},{'$set':update_data})
    room = room_collection.find_one({"_id":ObjectId(room_id)})
    room['_id'] = str(room['_id'])
    return jsonify(room), 200
@app.route('/room/<room_id>',methods=['DELETE'])
def delete_room(room_id):
    result = room_collection.delete_one({"_id":ObjectId(room_id)})
    if result.deleted_count > 0:
        return jsonify({"message":"Room deleted"}), 200
    else:
        return jsonify({"error":"Room not found"}), 404