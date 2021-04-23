from flask import request, Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug import exceptions
from werkzeug.datastructures import ImmutableMultiDict

import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
import models
import responses

# Ensure the DB is able to determine migration needs.
migrate = Migrate(app, db, compare_type=True)
with app.test_request_context():
    db.init_app(app)
    db.create_all()


action_list = {
    "webApi_document_template": responses.document_template,
    "webApi_area_list": responses.area_list,
    "webApi_category_list": responses.category_list,
    "webApi_area_shopinfo": responses.shop_info,
    "webApi_shop_list": responses.shop_list,
    "webApi_shop_one": responses.shop_one,
    "webApi_menu_list": responses.menu_list,
    "webApi_item_list": responses.item_list,
    "webApi_item_one": responses.item_one,
    "webApi_Authkey": responses.auth_key,
    "webApi_basket_list": responses.basket_list,
    "webApi_basket_reset": responses.basket_reset,
}


@app.route("/nwapi.php", methods=["GET"])
def api():
    try:
        # These values should be consistent for both v1 and v512.
        if request.args["platform"] != "wii":
            return exceptions.BadRequest()

        action = request.args["action"]
        return action_list[action](request)
    except KeyError:
        # This is not an action or a format we know of.
        return exceptions.NotFound()


def print_multi(passed_dict):
    if isinstance(passed_dict, ImmutableMultiDict):
        passed_dict = passed_dict.items(multi=True)

    for key, value in passed_dict:
        try:
            # Encode as UTF-8
            value = value.encode("shift-jis").decode("utf-8")
            print(f"{key} -> {value}")
        except Exception as e:
            # If it errors, leave as is with a note.
            print(f"An error occurred while decoding key {e}")
            print(f"Its value is '{value}' (not decoded)")


@app.route("/nwapi.php", methods=["POST"])
def error_api():
    print("Received an error!")

    print_multi(request.args)
    print_multi(request.form)

    return action_list["webApi_document_template"](request)


@app.route("/itemimg/<filename>")
@app.route("/logoimg2/<filename>")
def serve_logo(filename):
    return send_from_directory("images", filename)


if __name__ == "__main__":
    app.run()
