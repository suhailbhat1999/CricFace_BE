from app.models.product import Products #, #UserCart #Category,
from app import db


class UserService:
    def get_all_items_db(self):
        all_products = Products.query.all()
        res = []
        print("all products", all_products)
        for pro in all_products:
            print("pro", pro)
            this_pro = {
                "product_id": pro.product_id,
                "itemName": pro.name,
                "rate": pro.rate,
                "quantity": pro.quantity,
                "desc": pro.desc
            }
            # categories = Category.query.filter_by(product_id=pro.id)
            # for cat in categories:
            #     this_pro["category"].append(cat.name)
            res.append(this_pro)
        print("res", res)
        return res

    # def add_cart_db(self, data):
    #     new_cart = UserCart(
    #         quantity=data["quantity"],
    #         amount=data["amount"],
    #         rate=data["rate"],
    #         product_id=data["product_id"],
    #         notes=data["notes"],
    #         # user_id=userId
    #     )
    #     db.session.add(new_cart)
    #     db.session.commit()
    #     return True

    # def get_cart_db(self):
    #     cart_items = UserCart.query.filter_by(
    #         user_id=).order_by(UserCart.id.desc())
    #     res = []
    #     for cart_item in cart_items:
    #         this_item = {
    #             "cart_id": cart_item.id,
    #             "quantity": cart_item.quantity,
    #             "rate": cart_item.rate,
    #             "amount": cart_item.amount,
    #             "notes": cart_item.notes,
    #             "product_id": cart_item.product_id
    #         }
    #         product = Product.query.filter_by(id=cart_item.product_id).first()
    #         if product:
    #             this_item["product_name"] = product.name
    #             this_item["quantity_available"] = product.quantity
    #             res.append(this_item)
    #     return res
    #
    # def edit_cart_db(self, userId, data):
    #     cart_item = UserCart.query.filter_by(
    #         id=data["cart_id"], user_id=userId).first()
    #     if cart_item:
    #         cart_item.amount = data["amount"]
    #         cart_item.quantity = data["quantity"]
    #         db.session.commit()
    #         return True
    #     else:
    #         return False
    #
    # def delete_cart_db(self, userId, cartId):
    #     cart_item = UserCart.query.filter_by(id=cartId, user_id=userId).first()
    #     if cart_item:
    #         db.session.delete(cart_item)
    #         db.session.commit()
    #         return True
    #     return False
