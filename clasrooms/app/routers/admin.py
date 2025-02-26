from quart import Blueprint,request,jsonify,websocket
import websockets
from app.services.admin import AdminService
from app.schemas.admin import DeleteStudent,GetsStudentByName,BookRoom,CancelBooking
from app.utils.check_role import is_admin

from app.services.active_connections import active_connections

router = Blueprint("/admin",__name__,url_prefix="/admin")

@router.route("/book_room",methods = ["POST"])
async def book_room():
    admin = await is_admin()
    if not admin:
        return jsonify({"error":"not authorized"}), 401
    book_room_info = await request.get_json()
    try:
        book_room_scheem = BookRoom(**book_room_info)
    except:
        return jsonify({"error":"enter valid values for buuking"}),400
    try:
        booking = await AdminService.book_room(book_room_info)
        return booking
    except:
        return jsonify({"error":"something went wrong"}), 400
    
@router.route("/cancel_booking",methods = ["POST"])
async def cancel_booking():
    admin =await is_admin()
    if not admin:
        return jsonify({"error":"not authorized"}),401
    booking_data = await request.get_json()
    booking_scheem = CancelBooking(*booking_data)
    cancellation = await AdminService.cancel_booking(booking_scheem)
    return cancellation

@router.route("/student",methods=["GET"])
async def get_all_students():
    try:
        admin = await is_admin()
        if not admin:
            return jsonify({"error":"not autharized"}),401
        students = await AdminService.get_all_students()
        return students
    except Exception:
        return jsonify({"error":"an error occured"}), 500

@router.route("/student_name",methods = ["GET"])
async def get_student_by_name():
    try:
        admin = await is_admin()
        if not admin:
            return jsonify({"error":"not authorized"}),401
        student_info = GetsStudentByName(**student_info)    
        students = await AdminService.get_student_by_name()
        return students
    except Exception:
        return jsonify({"error":"an error has occured"})

@router.route("/students_delete",methods=["DELETE"])
async def delete_student():
    try:
        admin = is_admin()
        if not admin:
            return jsonify({"error":"not authorized"}),401
        student_info = await request.get_json()
        student_info_scheem = DeleteStudent(**student_info)

        delete_student = await AdminService.delete_student(student_info_scheem)
        return delete_student
    except Exception:
        return jsonify({"error":"something went wrong"}),400
    
@router.rout("/create_student",methods="POST")
async def create_student():
    try:
        admin = await is_admin()
        if not admin:
            return jsonify({"error":"not authorized"}),400
        arguments = await request.get_json()
        new_student = await AdminService.create_student(arguments)
        return jsonify(new_student)
    except Exception:
        return jsonify({"error":"an error has occured"}), 500

@router.route("/notifications",methods = ["GET"])
async def notifications():
    try:
        async with websocket.connect("ws://124.0.0.1:5000/ws") as ws:
            await ws.send("admin connected")
            msg = await ws.recv()
            return jsonify({"message":msg})
    except Exception as e:
        return jsonify({"error":"failed to connect to websocket"}),500

@router.websocket("/ws")
async def admin_ws():
    connection = websocket._get_current_object()
    active_connections.add(connection)
    try: 
        while True:
            message = await websocket.receive()
            await websocket.send(f"message recieved:{message}")
    except Exception as e:
        return jsonify({"error":f"websocket error:{e}"})
    finally:
        active_connections.remove(connection)

async def broadcast_to_admin(message:str):
    for connection in list(active_connections):
        try:
            await connection.send(message)
        except Exception as e:
            active_connections.remove(connection)

@router.websocket("/student_ws")
async def student_ws():
    connection = websocket._get_current_object()
    active_connections.add(connection)

    try:
        while True:
            message = await websocket.receive()
            await broadcast_to_admin(f"notification for student:{message}")
    except Exception as e:
        return jsonify({"error":f"websocket error:{e}"})
    finally:
        active_connections.remove(connection)
