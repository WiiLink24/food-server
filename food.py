from flask import request, Flask, send_from_directory
from werkzeug import exceptions

import responses

app = Flask(__name__)

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


@app.route("/nwapi.php", methods=["POST"])
def error_api():
    print("Received an error!")

    for key, value in request.args.items(multi=True):
        try:
            # Encode as UTF-8
            value = value.encode("shift-jis").decode("utf-8")
            print(f"{key} -> {value}")
        except Exception as e:
            # If it errors, leave as is with a note.
            print(f"An error occurred while decoding: {e}")
            print(f"{key} -> {value} (not decoded)")

    for key, value in request.form.items(multi=True):
        try:
            # Encode as UTF-8
            value = value.encode("shift-jis").decode("utf-8")
            print(f"{key} -> {value}")
        except Exception as e:
            # If it errors, leave as is with a note.
            print(f"An error occurred while decoding: {e}")
            print(f"{key} -> {value} (not decoded)")

    return action_list["webApi_document_template"](request)


@app.route("/itemimg/<filename>")
@app.route("/logoimg2/<filename>")
def serve_logo(filename):
    return send_from_directory("./images", filename)


if __name__ == "__main__":
    app.run()
