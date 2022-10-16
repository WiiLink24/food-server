import enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
import sqlalchemy, json

db = SQLAlchemy()
login = LoginManager()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


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

class ShopRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)


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


class User(db.Model, UserMixin):
    # Used to login to the Admin Panel
    id = db.Column(db.Integer, primary_key=True, default=1)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@listens_for(User.__table__, "after_create")
def create_default_user(target, connection, **kw):
    """Adds a default user to The Pantry.
    By default, we assume admin:admin."""
    table = User.__table__
    connection.execute(
        table.insert().values(
            username="admin",
            password_hash=generate_password_hash("admin"),
        )
    )
