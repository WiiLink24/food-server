import sentry_sdk

from flask import request, Flask, send_from_directory
from flask_migrate import Migrate
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug import exceptions
from werkzeug.datastructures import ImmutableMultiDict

from models import db

import config

if config.use_sentry:
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        integrations=[FlaskIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0,
    )

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = config.secret_key
app.config["OIDC_CLIENT_SECRETS"] = config.oidc_client_secrets_json
app.config["OIDC_SCOPES"] = "openid profile"
app.config["OIDC_OVERWRITE_REDIRECT_URI"] = config.oidc_redirect_uri

# Ensure DB tables are created.
db.init_app(app)

# Ensure the DB is able to determine migration needs.
migrate = Migrate(app, db, compare_type=True)


with app.app_context():
    # Ensure our database is present.
    db.create_all()


# Import functions with routes.
# TODO(spotlightishere): Convert to blueprints
import responses
import thepantry

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
    "webApi_Authkey": responses.generate_auth_key,
    "webApi_basket_list": responses.basket_list,
    "webApi_basket_reset": responses.basket_reset,
    "webApi_basket_add": responses.basket_add,
    "webApi_validate_condition": responses.validate_condition,
    "webApi_order_done": responses.order_done,
    "webApi_inquiry_done": responses.inquiry_done,
    "webApi_basket_delete": responses.basket_delete,
    "webApi_basket_modify": responses.basket_modify,
}


@app.route("/nwapi.php", methods=["GET"])
def base_api():
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
    if request.form.get("action") is None:
        print("Received an error!")

        print_multi(request.args)
        print_multi(request.form)

        return action_list["webApi_document_template"](request)

    try:
        # These values should be consistent for both v1 and v512.
        if request.form["platform"] != "wii":
            return exceptions.BadRequest()

        action = request.form["action"]
        return action_list[action](request)
    except KeyError:
        # This is not an action or a format we know of.
        return exceptions.NotFound()


if app.debug:

    @app.route("/logoimg2/<filename>")
    def serve_logo(filename):
        return send_from_directory("images", filename)

    @app.route("/itemimg/<category_code>/<filename>")
    def serve_food_image(category_code, filename):
        return send_from_directory(f"images/{category_code}/", filename)
