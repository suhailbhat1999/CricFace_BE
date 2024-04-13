from flask import Blueprint
from app.controllers.manager_controller import get_all_products, add_product, upload_image, delete_image,update_product, delete_product, \
    update_order, get_all_orders, delete_order

manager_routes = Blueprint('manager', __name__, url_prefix="/api/manager")

manager_routes.route("/get_all_products", methods=["GET"])(get_all_products)
manager_routes.route("/add_product", methods=["POST"])(add_product)
manager_routes.route("/upload_image/<int:prod_id>", methods=["POST"])(upload_image)
manager_routes.route("/update_product", methods=["POST"])(update_product)
manager_routes.route("/delete_product/<int:product_id>", methods=["DELETE"])(delete_product)
manager_routes.route("/update_order/<int:order_id>", methods=["POST"])(update_order)
manager_routes.route("/get_all_orders", methods=["GET"])(get_all_orders)
manager_routes.route("/delete_order/<int:order_id>", methods=["DELETE"])(delete_order)
manager_routes.route("/delete_image/<int:product_id>", methods=["DELETE"])(delete_image)

