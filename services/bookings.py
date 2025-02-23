from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("")
db = client["dbname"]

users_collection = db['users']
rooms_collection = db['rooms']
bookings_collection = db["bookings"]

@app.route('/bookings',methods=['POST'])
def create_booking(user_id,room_id):
    data = request.get_json()
    if 'user_id' not in data or 'room_id' not in data:
        return jsonify({"error":"user_id and room_id are required"}), 400
    
    user = users_collection.find_one({"_id": ObjectId(data[user_id])})
    room = rooms_collection.find_one({"_id": ObjectId(data[room_id])})

    if not user:
        return jsonify({"error":"user not found"})
    if not room:
        return jsonify({"error":"room not found"})
    
    booking = {
        "user_id": data["user_id"],
        "room_id": data["room_id"],
        "booking_date": data["booking_date"],
        "status":"booked"
        }
    
    result = bookings_collection.insert_one(booking)
    booking["_id"]=str(result.inserted_id)

    return jsonify(booking), 201

@app.route('/bookings',methods=['GET'])
def get_bookings():
    bookings = []
    for booking in bookings_collection.find():
        booking['_id'] = str(booking['_id'])
        bookings.append(booking)
    return jsonify(bookings), 200

@app.route('/bookings/<booking_id>', methods = ['GET'])
def get_booking_by_id(booking_id):
    booking = bookings_collection.find_one({'_id':ObjectId(booking_id)})
    if booking:
        booking['_id'] = str(booking['_id'])
        return jsonify(booking), 200
    else:
        return jsonify({"error":"booking not found"}), 404

@app.route('/booking/<booking_id>',methods = ['PUT'])
def Update_booking(user_id,booking_id):
    data = request.get_json()
    
    booking = bookings_collection.find_one({"_id":ObjectId(booking_id)})
    if not booking:
        return jsonify({"error":"booking not found"}), 404

    update_data = {}
    if user_id == booking['user_id']:
        if 'room_id' in data:
            update_data['room_id'] = data['room_id']
        if 'booking_date' in data:
            update_data['booking_date'] = data['booking_date']
        if 'booking_start' in data:
            update_data['booking_start'] = data['booking_start']
        if 'booking_end' in data:
            update_data['booking_end'] = data['booking_end']
        if 'status' in data:
            update_data['status'] = data['status']
    
    bookings_collection.update_one({"_id":ObjectId(booking_id)},{"$set":update_data})
    booking = bookings_collection.update_one({"_id":ObjectId(booking_id)})
    booking['_id'] = str(booking['_id'])
    return jsonify(booking), 200

@app.route('/booking/<booking_id>', methods = ['DELETE'])
def delete_booking(booking_id):
    result = bookings_collection.delete_one({"_id": ObjectId(booking_id)})
    if result.delete_count>0:
        return jsonify({"message": "booking deleted successfully"}), 200
    else:
        return jsonify({"error":"booking not found"})