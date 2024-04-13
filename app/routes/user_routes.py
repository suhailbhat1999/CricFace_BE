from flask import Blueprint
from app.controllers.user_controller import get_all_products , order_now#, add_to_cart, get_cart_items, edit_cart_item, delete_cart_item
user_routes = Blueprint('user', __name__, url_prefix="/api/user")

user_routes.route("/get_all_products", methods=["GET"])(get_all_products)
user_routes.route("/add_order", methods=["POST"])(order_now)
# user_routes.route("/get_all_cart_items", methods=["GET"])(get_cart_items)
# user_routes.route("/edit_cart_item", methods=["POST"])(edit_cart_item)
# user_routes.route("/delete_cart_item/<int:cart_id>", methods=["DELETE"])(delete_cart_item)
