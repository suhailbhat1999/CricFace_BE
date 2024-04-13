import logging
import os.path
import shutil
from app.models.product import Products, Orders
from Logging import logger
from app import db


class ManagerService:

    @staticmethod
    def get_all_products():
        res = []
        try:
            manager_products = Products.query.all()
            for pro in manager_products:
                this_pro = {
                    "id": pro.product_id,
                    "itemName": pro.name,
                    "rate": pro.rate,
                    "desc": pro.desc
                }
                res.append(this_pro)
        except Exception as e:
            logger.exception(f"Error while fetching the products : {e}")
        return res

    @staticmethod
    def add_new_product(data):
        try:
            new_product = Products(name=data["name"], rate=data["rate"], desc=data["desc"])
            db.session.add(new_product)
            db.session.commit()
            db.session.commit()
            return new_product.product_id
        except Exception as e:
            logging.exception(f"Error while adding new product {data} : {e}")
            return False

    @staticmethod
    def edit_product(data):
        try:
            product = Products.query.filter_by(product_id=data["product_id"]).first()
            if product:
                product.name = data["name"]
                product.rate = data["rate"]
                product.quantity = data["quantity"]
                product.desc = data["desc"]

                db.session.commit()
                return True

            else:
                logger.warning(f"Could not find the prod details for : {data}")
                return False
        except Exception as e:
            logger.exception(f"Error while editing the order : {e}")

    def delete_product(self, product_id):
        try:
            product = Products.query.filter_by(product_id=product_id).first()
            if product:
                db.session.delete(product)
                db.session.commit()
                self.del_prod_details(product_id)
                return True
            return False
        except Exception as e:
            logger.exception(f"Error while deleting the product with product id : {product_id} : {e}")

    def del_prod_details(self, id):
        folder_path = os.path.join("assets/images", str(id))
        try:
            # Delete the folder and its contents
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"Folder '{folder_path}' deleted successfully.")
        except OSError as e:
            logger.exception(f"Error while deleting the folder : {folder_path} : {e.strerror}")


    def delete_image(self, id, image_name=None, is_primary=False):
        if is_primary:
            folder_path = os.path.join("assets/images/", str(id), "pri_image")
            try:
                # List all files in the folder
                files = os.listdir(folder_path)

                # Iterate through each file and remove it
                for file_name in files:
                    file_path = os.path.join(folder_path, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        logger.info(f"File '{file_path}' removed successfully.")
                        return True
            except OSError as e:
                logger.exception(f"Error while deleting the image in path {folder_path} : {e.strerror}")
                return False
        else:
            image_path = os.path.join("assets/images/", str(id), "sec_images", image_name)
            try:
                if os.path.isfile(image_path):
                    os.remove(image_path)
                    logger.info(f"File {image_name} removed successfully")
                    return True
            except Exception as e:
                logger.exception(f"Error while deleting the image with path {image_path} : {e}")
                return False

    @staticmethod
    def get_all_orders():
        try:
            order_list = Orders.query.all()
            res = []

            for each_order in order_list:
                this_pro = {
                    "id": each_order.id,
                    "username": each_order.username,
                    "amount": each_order.amount,
                    "quantity": each_order.quantity,
                    "desc": each_order.desc,
                    "number": each_order.number,
                    "address": each_order.address,
                    "email": each_order.email,
                    "amt_paid": each_order.paid_amt,
                    "order_date": each_order.date,
                }
                res.append(this_pro)
            return res
        except Exception as e:
            logger.exception(f"Error while fetching the order list : {e}")

    @staticmethod
    def update_order(data, order_id):
        try:
            order = Orders.query.filter_by(id=order_id).first()
            if order:
                if "name" in data:
                    order.name = data["name"]
                if "amount" in data:
                    order.amount = data["amount"]
                if "quantity" in data:
                    order.quantity = data["quantity"]
                if "status" in data:
                    order.status = data["status"]
                if "address" in data:
                    order.address = data["address"]
                if "number" in data:
                    order.number = data["number"]
                if "email" in data:
                    order.email = data["email"]
                if "amt_paid" in data:
                    order.paid_amt = data["amt_paid"]

            db.session.commit()
            return True
        except Exception as e:
            logger.exception(f"Error while updating order with order details {data} :  {e}")

    @staticmethod
    def delete_order(order_id):

        try:
            order = Orders.query.filter_by(id=order_id).first()
            if order:
                db.session.delete(order)
                logger.info(f"Order delete with order id {order_id} successful.")
                db.session.commit()
                return True
            return False
        except Exception as e:
            logger.exception(f"Error while deleting the order with order id {order_id} : {e} ")
