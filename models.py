import enum

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy, json

db = SQLAlchemy()


class DictType(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.Text()

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class CategoryTypes(enum.Enum):
    Pizza = 1
    Bento_Box = 2
    Sushi = 3
    Fish = 4
    Seafood = 5
    Western = 6
    Fast_Food = 7
    Curry = 8
    Party_Food = 9
    Drinks = 10
    Others = 11

    @classmethod
    def choices(cls):
        return [(choice, choice.name.replace("_", " ")) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(int(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)


class Shops(db.Model):
    name = db.Column(db.String, nullable=False)
    category_code = db.Column(db.Enum(CategoryTypes), nullable=False)
    description = db.Column(db.String, nullable=False)
    shop_code = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    wait_time = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String, nullable=False)
    amenity = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)


class MenuList(db.Model):
    menu_code = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    title = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    shop_code = db.Column(db.Integer, db.ForeignKey("shops.shop_code"), nullable=False)


class ItemList(db.Model):
    item_code = db.Column(db.Integer, nullable=False, primary_key=True)
    menu_code = db.Column(
        db.Integer, db.ForeignKey("menu_list.menu_code"), nullable=False
    )
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)


class UserOrders(db.Model):
    zip_code = db.Column(db.String, primary_key=True, nullable=False)
    auth_key = db.Column(db.String)
    basket = db.Column(DictType, nullable=False)
