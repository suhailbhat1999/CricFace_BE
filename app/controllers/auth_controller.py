import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request
from app.services.auth_service import AuthService
from app.utils import build_cors_preflight_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_service = AuthService()


def login():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()
        
        content_type = request.headers.get('Content-Type')
        if not (content_type == 'application/json'):
            return {"message": "Wrong input format, only JSON allowed"}, 400
        
        data = request.get_json()
        print("data login", type(data))
        if not ("username" in data and "password" in data):
            return {"message": "Missing important information"}, 400
        if not (data["username"] and data["password"]):
            return {"message": "Email and Password cannot be empty"}, 400
        
        user = auth_service.get_user_by_email(data["username"])

        if user == False:
            return {"message": "Something went wrong"}, 500
        # if user and sha256.verify(data["password"], data["password"]):
        if data["password"] == "admin" and data["username"] == "admin":
        #     access_token = create_access_token(1)
        #     print("access token", access_token)
        #     refresh_token = create_refresh_token(1)
        #     print("refresh token", refresh_token)
            return {
                "user_name": user["username"],
                "user_role": "admin", #user["user_role"],
                "access_token": "sdfasdfasasccf", #access_token,
                "refresh_token": 4123412,#refresh_token
                "status": "success",
                "message": "Login Successful"
                }, 200
        else:
            return {"message": "Wrong crediantials", "status": "Failed"}, 401
    except Exception as e:
        print(traceback.print_exc(e))
        return {"message": "Something went wrong"}, 500
    
@jwt_required(refresh=True)
def refresh_token():
    try:
        if request.method == "OPTIONS":
                return build_cors_preflight_response()
            
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}, 200
    except Exception as e:
        print(traceback.print_exc(e))
        return {"message": "Something went wrong"}, 500
    