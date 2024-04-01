import traceback
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request
from app.services.manager_service import ManagerService
from app.utils import build_cors_preflight_response
from flask_jwt_extended import jwt_required, get_jwt_identity

manager_service = ManagerService()

# @jwt_required()
def get_all_products():
    try:
        # userId = get_jwt_identity()
        products = manager_service.get_all_products_db()
        return {"data":products}, 200
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
    
# @jwt_required()
def add_product():
    try:
        # userId = get_jwt_identity()

        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400
        
        data = request.get_json()
        print("data is ", data)
        if not ("name" in data and "rate" in data and "quantity" in data and "desc" in data):
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.add_product_db(data)
        if status:
            return {"message": "successfully added the item"}, 200
        return {"message": "something went wrong"}, 500
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
    
# @jwt_required()
def edit_product():
    try:
        # userId = get_jwt_identity()
        content_type = request.headers.get("Content-Type")
        if not content_type == "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()
        print("data to eidt", data)
        if not ("product_id" in data and "name" in data and "rate" in data and "quantity" in data):
            return {"message": 'Missing data in the request'}, 400
        status = manager_service.edit_product_db(data)
        if status:
            return {"message": "successfully updated the item"}, 200
        return {"message": "something went wrong"}, 500
    
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500
    
# @jwt_required()
def delete_product(product_id):
    try:
        # userId = get_jwt_identity()
        print("po", product_id)
        status = manager_service.delete_product_db(product_id)
        if status:
            return {"message": "successfully deleted the item"}, 200
        return {"message": "something went wrong"}, 500
    
    except Exception as e:
        traceback.print_exc(e)
        return {"message": "Something went wrong"}, 500