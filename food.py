from flask import request, Flask
from werkzeug import exceptions

import responses

app = Flask(__name__)

action_list = {
    "webApi_document_template": responses.document_template,
    "webApi_area_list": responses.area_list,
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
        print(f"{key} -> {value}")

    return ""


if __name__ == "__main__":
    app.run()
