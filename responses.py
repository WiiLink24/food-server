from helpers import xml_response


@xml_response()
def document_template():
    return {
        "apiStatus": {"code": 0},
        "container0": {"contents": "no terms and conditions"},
        "container1": {"contents": "no seriously, stop trying"},
        "container2": {"contents": "the heck are you doing"},
        "version": 1,
    }
