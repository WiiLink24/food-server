from lxml import etree
from werkzeug import exceptions

from helpers import (
    response,
    dict_to_etree,
    multiple_root_nodes,
    get_restaurant,
)


@multiple_root_nodes()
def basket_reset(request):
    return {}


@multiple_root_nodes()
def basket_list(request):
    return {
        "basketPrice": "99999.99",
        "chargePrice": "999999999",
        "discountPrice": "999999999",
        "totalPrice": 1,
        "Status": {"isOrder": 1, "messages": {"hey": "how are you?"}},
        "List": {
            "generic": {
                "basketNo": 1,
                "menuCode": 1,
                "itemCode": 1,
                "name": "Pizza Hut",
                "price": 1,
                "size": 1,
                "isSoldout": 0,
                "quantity": 1,
                "subTotalPrice": 1,
                "Menu": {
                    "name": "Menu",
                    "lunchMenuList": {
                        "isLunchTimeMenu": 1,
                        "isOpen": 1,
                    },
                },
                "optionList": {
                    "testing": {
                        "info": "Known to blow up in your face",
                        "code": 1,
                        "type": 1,
                        "name": "Pizza Hut",
                        "list": {
                            "item_one": {
                                "name": "Item One",
                                "menuCode": 1,
                                "itemCode": 1,
                                "image": 1,
                                "isSoldout": 0,
                                "info": "Known to blow up in your face",
                                "price": "5.99",
                            }
                        },
                    }
                },
            }
        },
    }


@multiple_root_nodes()
def auth_key(request):
    return {
        "authKey": "lol",
    }


@multiple_root_nodes()
def item_one(request):
    return {
        "price": "5.99",
        "optionList": {
            "testing": {
                "info": "Known to blow up in your face",
                "code": 1,
                "type": 1,
                "name": "Pizza Hut",
                "list": {
                    "item_one": {
                        "name": "Item One",
                        "menuCode": 1,
                        "itemCode": 1,
                        "image": 1,
                        "isSoldout": 0,
                        "info": "Known to blow up in your face",
                        "price": "5.99",
                    }
                },
            }
        },
    }


@multiple_root_nodes()
def item_list(request):
    return {
        "Count": 1,
        "List": {
            "container0": {
                "name": "Hello!!!!",
                "item": {
                    "menuCode": 1,
                    "itemCode": 1,
                    "price": "5.99",
                    "info": "Not known to the state of California to cause cancer",
                    "size": 1,
                    "image": 1,
                    "isSoldout": 0,
                    "sizeList": {
                        "itemCode": 1,
                        "size": 1,
                        "price": "5.99",
                        "isSoldout": 0,
                    },
                },
            }
        },
    }


@multiple_root_nodes()
def menu_list(request):
    return {
        "response": {
            "testing": {
                "menuCode": 1,
                "linkTitle": "Mmmm food",
                "enabledLink": 1,
                "name": "Yeah! Good food.",
                "info": "Screamingly delightful.",
                "setNum": 0,
                "lunchMenuList": {
                    "isLunchTimeMenu": 1,
                    "hour": {
                        "start": 1,
                        "end": 1,
                    },
                    "isOpen": 1,
                },
                "message": "Where does this show up?",
            },
            "testing_two": {
                "menuCode": 2,
                "linkTitle": "More food!",
                "enabledLink": 1,
                "name": "Amazing food",
                "info": "Screamingly delightful.",
                "setNum": 0,
                "lunchMenuList": {
                    "isLunchTimeMenu": 1,
                    "hour": {
                        "start": 1,
                        "end": 1,
                    },
                    "isOpen": 1,
                },
                "message": "Where does this show up?",
            },
        }
    }


@multiple_root_nodes()
def shop_one(_):
    return {
        "response": {
            "categoryCode": "02",
            "address": "123 Four Five Ln.",
            "attention": "Your attention please.",
            "amenity": "Free mints with all orders",
            "menuListCode": 1,
            "activate": "on",
            "waitTime": 1,
            "timeorder": 1,
            "tel": "1478640183279",
            "yoyakuMinDate": 1,
            "yoyakuMaxDate": 2,
            "paymentList": {"athing": "Fox Card"},
            "shopStatus": {
                "hours": {
                    "all": {
                        "message": "We never close.",
                    },
                    "today": {
                        "values": {
                            "start": "12:34:56",
                            "end": "12:34:56",
                            "holiday": "n",
                        }
                    },
                    "delivery": {
                        "values": {
                            "start": "12:34:56",
                            "end": "12:34:56",
                            "holiday": "n",
                        }
                    },
                    "holiday": {
                        "status": {
                            "isOpen": 1,
                        }
                    },
                },
                "selList": {"values": {"id": 1, "name": "test"}},
            },
            "interval": 1,
        },
        "recommendItemList": {
            "container0": {
                "menuCode": 1,
                "itemCode": 1,
                "name": "AAAA",
                "price": 1,
                "info": "Freshly charred",
                "size": 1,
                "image": 1,
                "isSoldout": 0,
                "sizeList": {
                    "itemCode": 1,
                    "name": "AAAA",
                    "price": 1,
                    "info": "Freshly charred",
                    "size": 1,
                    "image": 1,
                    "isSoldout": 0,
                },
            },
        },
    }


@response()
def shop_info(request):
    # Return a blank dict for now
    return {}


@response()
def shop_list(request):
    return category_list(request)


@response()
def document_template(request):
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


def formulate_restaurant(category_id: int) -> dict:
    return {
        "LargeCategoryName": "Meal",
        "CategoryList": {
            "TestingCategory": {
                "CategoryCode": f"{category_id:02}",
                "ShopList": {"Shop": get_restaurant(category_id)},
            }
        },
    }


@multiple_root_nodes()
def category_list(_):
    # TODO: formulate properly
    return {
        "response": {
            "Pizza": formulate_restaurant(1),
            "Bento": formulate_restaurant(2),
            "Sushi": formulate_restaurant(3),
            "Fish": formulate_restaurant(4),
            "Seafood": formulate_restaurant(5),
            "American": formulate_restaurant(6),
            "Fast": formulate_restaurant(7),
            "Indian": formulate_restaurant(8),
            "Party": formulate_restaurant(9),
            "Drinks": formulate_restaurant(10),
            "Other": formulate_restaurant(11),
            "Placeholder": formulate_restaurant(12),
        }
    }


@multiple_root_nodes()
def basket_add(_):
    return {
        "Count": {
            "List": {
                "container0": {
                    "itemCode": 1,
                    "name": "AAAA",
                    "price": 1,
                    "info": "Freshly charred",
                    "size": 1,
                    "image": 1,
                    "isSoldout": 0,
                }
            }
        }
    }


@multiple_root_nodes()
def validate_condition(_):
    return {}


@multiple_root_nodes()
def order_done(_):
    return {}