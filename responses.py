from lxml import etree

from helpers import response, dict_to_etree


@response()
def document_template():
    return {
        "container0": {"contents": "no terms and conditions"},
        "container1": {"contents": "no seriously, stop trying"},
        "container2": {"contents": "the heck are you doing"},
    }


def area_list():
    @response()
    def actual_area_list():
        return {
            "areaList": {
                "place": {
                    "segment": "segment title",
                    "list": {"areaPlace": {"areaName": "place name", "areaCode": 1}},
                }
            },
            "areaCount": 1,
        }

    # Nintendo for whatever reason require a separate "selectedArea" element
    # as a root node within output.
    # This violates about every XML specification in existence.
    # I am reasonably certain there was a mistake as their function to
    # interpret nodes at levels accepts a parent node, to which they seem to
    # have passed passed NULL instead of response.

    # We are not going to bother spending time to deal with this.
    area_list_output = actual_area_list()

    selected_area = dict_to_etree("selectedArea", {"areaCode": 0})
    selected_area_output = etree.tostring(selected_area, pretty_print=True)

    return area_list_output + selected_area_output
