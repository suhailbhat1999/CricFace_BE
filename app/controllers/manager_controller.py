import os
import traceback
import jsonify
from passlib.hash import pbkdf2_sha256 as sha256
from flask import request
from Logging import logger
from app.services.manager_service import ManagerService
from app.utils import build_cors_preflight_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import save_image

manager_service = ManagerService()


@jwt_required()
def get_all_products():
    try:
        userId = get_jwt_identity()
        products = manager_service.get_all_products()
        return {"data": products}, 200
    except Exception as e:
        logger.exception(f"Error while fetching the products : {e}")
        return {"message": "Something went wrong"}, 500


@jwt_required()
def add_product():
    try:
        userId = get_jwt_identity()

        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"message": 'Only JSON allowed'}, 400

        data = request.get_json()

        if "name" not in data or "rate" not in data or "desc" not in data:
            logger.warning("payload missing some details, please check the payload")
            return {"message": 'Missing data in the request'}, 400
        logger.info(f"Adding new product : {data}")
        prod_id = manager_service.add_new_product(data)
        if prod_id:
            logger.info("New product added successfully")
            return {"message": f"successfully added new product", "status": "Success", "prod_id": prod_id}, 200
        logger.warning("Error while adding new product")
        return {"message": "something went wrong", "status": "Failed", "prod_id": False}, 500
    except Exception as e:
        logger.exception(f"Error while adding new product : {e}")
        return {"message": "Something went wrong", "status": "Failed", "prod_id": False}, 500


# @jwt_required()
def upload_image(prod_id):
    is_primary = request.form.get("is_primary")
    try:
        if is_primary == 1:
            folder_path = os.path.join("assets/images/", str(prod_id), "pri_image")
        else:
            folder_path = os.path.join("assets/images/", str(prod_id), "sec_images")

        os.makedirs(folder_path, exist_ok=True)
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'Error': 'No selected file'}), 400
        filename = file.filename
        file_path = os.path.join(folder_path, filename)
        file.save(file_path)
        # Return success message
        return jsonify({'message': 'File uploaded successfully', 'filename': filename}), 200

    except Exception as e:
        return jsonify({'error': f'Something went wrong: {str(e)}'}), 500

# Example usage:
# upload_image(prod_id=123, is_primary=True)


@jwt_required()
def get_product_details(prod_id):
    try:
        userId = get_jwt_identity()
        products = manager_service.fetch_prod_details(prod_id)
        if products:
            logger.info(f"Product details fected for product id {prod_id} ")
            return {"data": products, "status": "Success"}, 200
        return {"data": [], "status": "Failed"}
    except Exception as e:
        logger.exception(f"Error while fetching  product details for prod id {prod_id} : {e}")
        return {"message": "Something went wrong"}, 500

@jwt_required()
def update_product(prod_id):
    try:
        # Uncomment for JWT token authentication
        userId = get_jwt_identity()

        # Ensure request content type is JSON
        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"message": 'Only JSON data allowed'}, 400

        # Parse JSON data from request body
        data = request.get_json()
        product_id = data.get("product_id")

        # Check if required fields are present
        required_fields = ["product_id", "name", "rate", "quantity"]
        if any(field not in data for field in required_fields):
            return {"message": 'Required data missing in the request'}, 400

        # Log payload received for editing the product
        logger.info(f"Editing product with ID: {product_id}, Data: {data}")

        # Attempt to edit the product
        status = manager_service.edit_product(data)

        # Handle success or failure of product editing
        if status:
            logger.info(f"Product with ID {product_id} updated successfully. Status: {status}")
            return {"message": f"Product with ID {product_id} updated successfully."}, 200
        else:
            logger.warning(f"Failed to update product with ID {product_id}")
            return {"message": "Failed to update product. Please try again later."}, 500

    except Exception as e:
        logger.exception(f"Error occurred while updating product : {e}")
        return {"message": "Internal server error. Please try again later."}, 500


@jwt_required()
def delete_product(product_id):
    try:
        userId = get_jwt_identity()
        logger.info(f"Deleteting the product with Prod_id  : {product_id}")
        status = manager_service.delete_product(product_id)
        if status:
            logger.info("Product deleted Successfully")
            return {"message": f"successfully deleted the product with prod_id as {product_id}",
                    "status": "Success"}, 200
        logger.warning("Something went wrong while deleting the product.")
        return {"message": "something went wrong", "status": "Failed"}, 500

    except Exception as e:
        logger.exception(f"Something went wrong while deleting the product : {e}.")
        return {"message": "Something went wrong", "status": "Failed"}, 500


# @jwt_required()
def get_all_orders():
    try:
        # userId = get_jwt_identity()
        logger.info("Fetching order details for Admin.")
        orders = manager_service.get_all_orders()
        logger.info("Order details fetched successfully.")
        return {"data": orders, "status": "Success"}, 200
    except Exception as e:
        logger.exception(f"Something went wrong while fetching the order details : {e}")
        return {"message": "Something went wrong", "status": "Failed"}, 500

@jwt_required()
def delete_image(product_id):
    try:
        # Check content type
        get_jwt_identity()
        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"message": "Only JSON allowed"}, 400

        data = request.get_json()

        logger.info(f"Deleting image for product ID: {product_id}; data: {data}")

        image_name = data.get("image_name")
        if not image_name:
            logger.warning(f"Insufficient details for deleting image for product ID: {product_id}")
            return {"message": "Insufficient details for deleting image"}, 400

        is_primary = data.get("is_primary")

        status = manager_service.delete_image(product_id, image_name=image_name, is_primary=is_primary)
        if status:
            return {"message": "Image deleted successfully", "status": "Success"}, 200

        else:
            return {"message": "Error while deleting image", "status": "Failed"}

    except Exception as e:
        logger.exception(f"Error while deleting image for product ID {product_id}: {e}")
        return {"message": "Something went wrong"}, 500

@jwt_required()
def update_order(order_id):
    try:
        userId = get_jwt_identity()
        content_type = request.headers.get("Content-Type")
        if content_type != "application/json":
            return {"message": "Only JSON allowed"}, 400

        data = request.get_json()
        logger.info(f"Updating order with order id {order_id} with details {data}.")

        required_fields = ["id", "username", "amount", "quantity"]
        if any(field not in data for field in required_fields):
            logger.warning("Details missing in the payload, please check the payload.")
            return {"message": "Missing data in the request", "status": "Failed"}, 400

        status = manager_service.update_order(data, order_id)

        if status:
            logger.info(f"Order details updated with status: {status}")
            return {"message": f"Successfully updated the order with order id: {order_id}", "status": "Success"}, 200

        logger.warning(f"Something went wrong while updating order with order id {order_id}.")
        return {"message": "Something went wrong", "status": "Failed"}, 500

    except Exception as e:
        logger.exception(f"Error while updating the order with order id {order_id}: {e}")
        return {"message": "Something went wrong", "status": "Failed"}, 500

@jwt_required()
def delete_order(order_id):
    try:
        userId = get_jwt_identity()
        logger.info(f"Deleting order with order id {id}.")
        status = manager_service.delete_order(order_id)
        if status:
            logger.info(f"Response while deleting the order with order id: {id}.: {status}")
            return {"message": f"successfully deleted the Order with order id : {order_id}", "status": "Success"}, 200
        logger.warning("Something went wrong while deleting the order")
        return {"message": "something went wrong", "status": "Falied"}, 500

    except Exception as e:
        logger.exception(f"Error while deleting the order : {e}")
        return {"message": "Something went wrong", "status": "Failed"}, 500
