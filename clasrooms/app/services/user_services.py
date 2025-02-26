from quart import jsonify,request,websocket
from app.database.connection import schedule_collection,user_collection
from app.schemas.student import MeetingRooms,LoginUser
from app.services.active_connections import active_connections

class StudentService:
    @staticmethod
    async def get_all_rooms():
        schedules = await schedule_collection.find()
        room_info = []

        for schedule in schedules:
            room_name = schedule["rooms"]["name"]

            room = {
                "start": schedule.get("start"),
                "end": schedule.get("end"),
                "group_name":schedule.get("group_name")
                }
            
            if room_name not in room_info:
                room_info[room_name]=[]
            room_info[room_name].append(room)

        return room_info
    
    @staticmethod
    async def filter_room(name: str, room_type: str):
        all_rooms = await StudentService.get_all_rooms()
        filtered_rooms={}

        for room_name,room_list in all_rooms.items():
            meeting_room = room_name in {room.value for room in MeetingRooms}
            category = "MeetingRoom" if meeting_room else " Classroom"
            if name.lower() == room_name == room_type.lower():
                filtered_rooms[room_name] = {
                    "category":category,
                    "schelude":room_list
                }
        return filtered_rooms
    
    async def login():
        try:
            arguments = await request.get_json()
            login_data = LoginUser(**arguments)
            existing_user = await user_collection.find_one({"secret_code":login_data.secret_code,"name": login_data.name})
            if existing_user:
                response = jsonify({"message":"login successfull"})
                response.status_code = 200
                response.role = existing_user.get("role")
                return response
            
            response = jsonify({"error":"invalid credentials"}), 400
            return response
        
        except Exception as e:
            response = jsonify({"error":f"error occured during login:{str(e)}"}), 400
            return response
        
    @staticmethod
    async def handle_websocket():
        connection = websocket._get_current_object()
        active_connections.add(connection)
        try:
            while True:
                await websocket.receive()
        except:
            pass
        finally:
            active_connections.remove(connection)