from lxml import etree
from werkzeug import exceptions

from helpers import response, response_with_no_footer, dict_to_etree, RepeatedElement, Yomi, Kana, CDATA, DontCDATAMii

@response()
def shopinfo(request):
    return {} # Return a blank dict for now
@response()
def document_template(request):
    # Observed to be true in v1 and v512.
    # Actually not, the version is different when making an order request
    if request.args.get("version") != "00000":
        # Dump request data
        print(request.args)
        print(request.json)
        

    return {
        "container0": {"contents": "no terms and conditions"},
        "container1": {"contents": "no seriously, stop trying"},
        "container2": {"contents": "the heck are you doing"},
    }


@response()
def area_list(request):
    if request.args.get("zipCode"):
        # Nintendo, for whatever reason, require a separate "selectedArea" element
        # as a root node within output.
        # This violates about every XML specification in existence.
        # I am reasonably certain there was a mistake as their function to
        # interpret nodes at levels accepts a parent node, to which they seem to
        # have passed passed NULL instead of response.
        #
        # We are not going to bother spending time to deal with this.
        @response()
        def area_list_only_segments():
            return {
                "areaList": {
                    "place": {
                        "segment": "segment title",
                        "list": {
                            "areaPlace": {"areaName": "place name", "areaCode": 2}
                        },
                    },
                },
                "areaCount": 1,
            }

        area_list_output = area_list_only_segments()

        selected_area = dict_to_etree("selectedArea", {"areaCode": 1})
        selected_area_output = etree.tostring(selected_area, pretty_print=True)

        return area_list_output + selected_area_output

    area_code = request.args.get("areaCode")
    if not area_code:
        # We expect either a zip code or an area code.
        return exceptions.BadRequest()

    if area_code == "0":
        # An area code of 0 is passed upon first search.
        return {
            "areaList": {
                "place": {
                    "segment": "segment title",
                    "list": {"areaPlace": {"areaName": "place name", "areaCode": 2}},
                },
            },
            "areaCount": 1,
        }

    if area_code == "2":
        # An area code of 0 is passed upon first search. All else is deterministic.
        return {
            "areaList": {
                "place": {
                    "container0": "aaaa",
                    "segment": "area_title",
                    "list": {
                        "areaPlace": {
                            "areaName": "place one",
                            "areaCode": 3,
                            "isNextArea": 0,
                            "display": 1,
                            "kanji1": "title",
                            "kanji2": "kanji2",
                            "kanji3": "two",
                            "kanji4": "three",
                        }
                    },
                },
            },
            "areaCount": 1,
        }

    return exceptions.NotFound()


@response()
def category_list(request):
    # TODO: What values can this be? 0 and 1 have been observed.
    # if request.args.get("reservationType") != "0":
    #     return exceptions.BadRequest()
    '''
    "BigBoiCategory":{
        "LargeCategoryName":"meal",
        "CategoryList": {
            "ACategory":{
                "CategoryCode": 1,
                "ShopList": {
                    "TheShopShop":{
                        "shopCode":1,
                        "homeCode":1,
                        "name":"You wanted a name?",
                        "catchphrase":"on",
                        "minPrice":1,
                        "yoyaku":1,
                        "activate":1,
                        "waitTime":1,
                        "paymentList":{
                            "athing":"hi" 
                        },
                        "shopStatus":{
                            "status":{
                                "isOpen":"1",
                            }
                        }
                    }
                }
            }
        }
    }
    removed because it doesn't work
    '''
    return {
        "BigBoiCategory":{
        "LargeCategoryName":"meal",
        "CategoryList": {
            "ACategory":{
                "CategoryCode": 1,
                "ShopList": {
                    "TheShopShop":{
                        "shopCode":1,
                        "homeCode":1,
                        "name":"You wanted a name?",
                        "catchphrase":"on",
                        "minPrice":1,
                        "yoyaku":1,
                        "activate":1,
                        "waitTime":1,
                        "paymentList":{
                            "athing":"hi" 
                        },
                        "shopStatus":{
                            "status":{
                                "isOpen":"1",
                            }
                        }
                    }
                }
            }
        }
    }
