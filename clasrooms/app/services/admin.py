import aiohttp
import pytz
from datetime import datetime
from quart import jsonify
from mongoengine import connect

from app.database.connection import user_collection,schedule_collection
from app.models.rooms import Room,Schedule
from app.models.users import User
from app.schemas.admin import BookRoom,CancelBooking
from app.schemas.student import UserSchema

from quart import websocket
from app.services.active_connections import active_connections

utc_timezone = pytz.UTC

connect("classrooms",host="mongodb://localhost:27017/classrooms")

class AdminService:
    @staticmethod
    async def get_all_students():
        users = await user_collection.find().to_list(length=None)
        if not users:
            return jsonify({"error":"student not found"}),404
        for user in users:
            user["_id"] = str(user["_id"])
        return users 
    
    @staticmethod
    async def delete_student(student_info):
        user = await user_collection.find_one({"_id":id})
        result = await user_collection.delete_one({'_id':id})
        if result.deleted_count>0:
            return jsonify({"message":"user deleted successfully"}), 200
        else:
            return jsonify({"error":"user not found"}), 404
        
    @staticmethod
    async def book_room(book_room_info:BookRoom):
        room = Room(name=book_room_info.room_name)

        start = datetime.strptime(book_room_info.start,"%H:%M").replace(second=0,microsecond=0)
        end = datetime.strptime(book_room_info.end,"%H:%M").replace(second=0,microsecond=0)

        start = utc_timezone.localize(start)
        end = utc_timezone.localize(end)

        schedule=Schedule(rooms=room,start=start,end=end,group_name=book_room_info.group_name,activity=book_room_info.activity)
        schedule_dict = schedule.to_dict()
        await schedule_collection.insert_one(schedule_dict) 

        return jsonify({"message":"room booked successfully"}), 200
    
    @staticmethod
    async def cancel_booking(cancel_room_booking:CancelBooking):
        start = datetime.strptime(cancel_room_booking.start,"%H:%M").replace(second=0,microsecond=0)
        end = datetime.strptime(cancel_room_booking.end,"%H:%M").replace(second=0,microsecond=0)
        
        start = utc_timezone.localize(start)
        end = utc_timezone.localize(end)

        result = await schedule_collection.delete_one({
            "room.name":cancel_room_booking.room_name,
            "start":start,
            "end":end
        })

        if result.deleted_count>0:
            return jsonify({"message":"booking deleted successfully"}), 200
        else:
            return jsonify({"error":"no match found"}), 404
        
    @staticmethod
    async def create_student(arguments):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://127.0.0.1:5000/gen/secret_code") as response:
                if response.status == 200:
                    data = await response.json()
                    arguments["secret_code"] = data.get("api_key")#might be issue here
                else:
                    return jsonify({"error":"failed to generate api key"}), 500
                
        user = UserSchema(**arguments)
        user_data = user.model_dump() if hasattr(user,"dict") else vars(user)

        user_db = User(**arguments).to_dict()
        await user_collection.insert_one(user_db)
        return {"message":"user added successfully"}
    
    @staticmethod
    async def handle_websocket():
        connection = websocket._get_current_object()
        active_connections.add(connection)
        try:
            while True:
                message = await websocket.receive()
                print(f"message recieved: {message}")
                await websocket.send(f"Echo:{message}")
        except Exception as e:
            print(f"websocket error: {e}")
        finally:
            active_connections.remove(connection)
            