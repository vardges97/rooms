class user_scheme ()
  name
  surname
  email
  role
  group
  secret_code: str

class room_reservation()
  user_name
  room_name
  start
  end
  capacity
  activity
  created_at

class cancel_room()
  user_name
  room_name

class login_user()
  secret_code:str
  name
