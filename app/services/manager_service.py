from app.models.product import Products
from app import db


class ManagerService:
    def get_all_products_db(self):
        manager_products = Products.query.all()
        res = []

        for pro in manager_products:
            this_pro = {
                "id": pro.product_id,
                "itemName": pro.name,
                "rate": pro.rate,
                "quantity": pro.quantity,
                "desc": pro.desc
            }
            # categories = Category.query.filter_by(product_id = pro.id)
            # for cat in categories:
            #     this_pro["category"].append(cat.name)
            res.append(this_pro)
        print("resp", res)
        return res
    
    def add_product_db(self, data):
        new_product = Products(name=data["name"], rate=data["rate"], quantity=data["quantity"], desc=data["desc"])
        db.session.add(new_product)
        db.session.commit()
        # for cat in data["category"]:
        #     new_cat = Category(name=cat, product_id=new_product.id)
        #     db.session.add(new_cat)
        db.session.commit()
        return True

    def edit_product_db(self, data):
        product = Products.query.filter_by(product_id=data["product_id"]).first()
        if product:
            product.name = data["name"]
            product.rate = data["rate"]
            product.quantity = data["quantity"]
            db.session.commit()
            return True
        else:
            return False

    def delete_product_db(self, product_id):
        product = Products.query.filter_by(product_id=product_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False