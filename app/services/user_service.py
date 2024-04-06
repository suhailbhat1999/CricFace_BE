from app.models.product import Products, Orders
from Logging import logger
from app import db


class UserService:
    @staticmethod
    def get_all_products():
        try:
            all_products = Products.query.all()
            res = []
            for pro in all_products:
                this_pro = {
                    "product_id": pro.product_id,
                    "itemName": pro.name,
                    "rate": pro.rate,
                    "desc": pro.desc
                }
                res.append(this_pro)
            return res
        except Exception as e:
            logger.exception(f"Error while fetching product list : {e}")

    @staticmethod
    def add_to_order(data):
        try:
            new_cart = Orders(
                quantity=data["quantity"],
                amount=data["amount"],
                desc=data["desc"],
                number=data["number"],
                email=data["email"],
                address=data["address"],
                date=data["date"],
                username=data["username"],
                status=data["status"],
                paid_amt=data["amt_paid"]
            )
            db.session.add(new_cart)
            db.session.commit()
            return True
        except Exception as e:
            logger.exception(f"error while adding {data} order details to table : {e}")
        return None
