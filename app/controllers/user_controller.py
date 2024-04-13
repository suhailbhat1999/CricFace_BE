import traceback
from flask import request
from datetime import datetime
from Logging import logger
from app.services.user_service import UserService

# from flask_jwt_extended import jwt_required, get_jwt_identity

user_service = UserService()


# @jwt_required()
def get_all_products():
    try:
        items = user_service.get_all_products()
        return {"data": items}, 200

    except Exception as e:
        logger.exception(f"Error while fetching the product list : {e}")
        return {"message": "Something went wrong"}, 500


# @jwt_required()
from datetime import datetime
import traceback


def order_now():
    try:
        # userId = get_jwt_identity()
        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        required_fields = ["amount", "username", "quantity", "desc", "number", "email", "address", "amt_paid"]
        if not all(field in data for field in required_fields):
            return {"message": 'Missing data in the request'}, 400

        if "date" not in data:
            data["date"] = datetime.now()

        status = user_service.add_to_order(data)

        if status:
            return {"message": "Successfully added to the cart", "status": "success"}, 200
        else:
            return {"message": "Something went wrong", "status": "Failed"}, 500

    except Exception as e:
        logger.exception(f"Error while placing order : :{e}")
        return {"message": "Something went wrong", "status": "Failed"}, 500


