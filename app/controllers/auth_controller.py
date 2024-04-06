import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request
from Logging import logger
from app.services.auth_service import AuthService
from app.utils import build_cors_preflight_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_service = AuthService()


def login():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            return {"message": "Wrong input format, only JSON allowed"}, 400

        data = request.get_json()
        if "username" not in data or "password" not in data:
            logger.warning(f"Missing important information in payload : {data}")
            return {"message": "Missing important information"}, 400
        if not (data["username"] and data["password"]):
            return {"message": "Email and Password cannot be empty"}, 400

        user = auth_service.get_user_by_email(data["username"])

        if user == False:
            logger.warning(f"Login Failed for : {data}")
            return {"message": "Something went wrong", "status": "Failed"}, 500
        # if user and sha256.verify(data["password"], data["password"]):
        if data["password"] == "admin" and data["username"] == "admin":
            access_token = create_access_token(1)
            refresh_token = create_refresh_token(1)
            logger.info(f"Login Successful for : {data}")
            return {
                       "user_name": user["username"],
                       "access_token": access_token,
                       "refresh_token": refresh_token,
                       "status": "Success",
                       "message": "Login Successful"
                   }, 200
        else:
            logger.warning(f"Login failed for : {data}")
            return {"message": "Wrong crediantials", "status": "Failed"}, 401
    except Exception as e:
        logger.exception(f"Error while login : {e}")
        return {"message": "Something went wrong"}, 500


@jwt_required(refresh=True)
def refresh_token():
    try:
        if request.method == "OPTIONS":
            return build_cors_preflight_response()

        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200
    except Exception as e:
        logger.exception(f"Error while refreshing token : {e}")
        return {"message": "Something went wrong"}, 500
