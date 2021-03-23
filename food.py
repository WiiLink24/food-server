from flask import request, Flask
from werkzeug import exceptions

import responses

app = Flask(__name__)

action_list = {
    "webApi_document_template": responses.document_template,
    "webApi_area_list": responses.area_list,
    "webApi_category_list": responses.actual_category_list,
    "webApi_area_shopinfo": responses.shopinfo,
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
    for key, value in request.form.items():
        try:
            # Encode as UTF-8
            print(f"{key} -> {value}".encode("utf-8"))
        except Exception as e:
            # If it errors, leave as is with a note.
            print(f"An error occurred while decoding: {e}")
            print(f"{key} -> {value} (not decoded)")

        return action_list["webApi_document_template"](request)


if __name__ == "__main__":
    app.run()
