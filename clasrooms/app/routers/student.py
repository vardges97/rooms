from quart import Blueprint, request, jsonify, make_response,session
from app.services.user_services import StudentService
from app.utils.util_functions import generate_secret_code_admin,generate_secret_code_student
from app.utils.check_role import is_student

from app.schemas.student import Roles

router = Blueprint("students",__name__,url_prefix="/classrooms")

@router.route("/",methods = ["GET"])
async def get_rooms():
    try:
        room = await StudentService.get_all_rooms()
        return jsonify(room)
    except Exception:
        return jsonify({"error":f"an error occured"}), 500
    
@router.route("/<name>/<type>")
async def get_room_by_name(name,type):
    try:
        room = await StudentService.filter_room(name,type)
        return jsonify(room)
    except Exception:
        return jsonify({"error":"an error has occured"}),500
    
@router.route("/login",methods=["POST"])
async def login():
    try:
        login_answer = await StudentService.login()
        if login_answer.status_code == 200:
            answer = await login_answer.json
            response = await make_response(answer)
            response.status_code = 200

            if login_answer.role == Roles.STUDENT.value:
                secret_code = generate_secret_code_student()
                response.headers["api_key"] = secret_code
                session["api_key"] = secret_code

            elif login_answer.role == Roles.ADMIN.value:
                secret_code = generate_secret_code_admin()
                response.headers["api_key"] = secret_code
                session["api_key"] = secret_code

            return response
        return login_answer
    except Exception as e:
        return jsonify({"error":f"something went wrong:{str(e)}"}), 500
    
@router.route("/logout",methods=["GET"])
async def logout():
    session.clear()
    return jsonify({"message":"logged out"})