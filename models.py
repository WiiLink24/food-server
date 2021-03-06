from food import db


class Shops(db.Model):
    name = db.Column(db.String, nullable=False, primary_key=True)
    category_code = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    shop_code = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, nullable=False)
    wait_time = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Boolean, nullable=False)
