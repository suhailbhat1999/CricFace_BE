from app import db


class Products(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rate = db.Column(db.Integer)
    desc = db.Column(db.String(255))
    # userid = db.Column(db.Integer, db.ForeignKey('users.id'))  # Define foreign key constraint
    # user = db.relationship('User', backref='products')


# class Category(db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Define foreign key constraint
#     product = db.relationship('Product', backref='category')

class Orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    desc = db.Column(db.String(300))
    date = db.Column(db.String(300))
    username = db.Column(db.String(300))
    email = db.Column(db.String(300))
    number = db.Column(db.String(300))
    address = db.Column(db.String(300))
    status = db.Column(db.String(50))  # New column for status
    paid_amt = db.Column(db.Integer)
    # product = db.relationship('Product', backref='user_cart')
