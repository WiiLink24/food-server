from datetime import datetime

from lxml import etree
from werkzeug import exceptions

from config import eula_text
from food import db
from uuid import uuid4
from models import Shops, MenuList, ItemList, UserOrders, CategoryTypes
from helpers import (
    response,
    dict_to_etree,
    multiple_root_nodes,
    get_restaurant,
    RepeatedElement,
    generate_random,
)


@response()
def inquiry_done(_):
    """The request a restaurant part.
    In the forms, it give us the telephone of the restaurant,
    name of the restaurant, and restaurant type.
    TODO: append to database"""

    return {}


@multiple_root_nodes()
def basket_reset(request):
    auth_key = request.args.get("authKey")
    query = UserOrders.query.filter_by(auth_key=auth_key).first()

    query.basket = []
    db.session.commit()
    return {"spot": True}


@multiple_root_nodes()
def basket_modify(request):
    num = request.form.get("basketNo")
    zip_code = request.form.get("areaCode")

    query = UserOrders.query.filter_by(zip_code=zip_code).first()
    basket = query.basket
    basket[int(num)]["qty"] = request.form.get("quantity")

    query.basket = []
    db.session.commit()

    query.basket = query.basket + basket
    db.session.commit()

    return {"food": True}


@multiple_root_nodes()
def basket_delete(request):
    num = request.args.get("basketNo")
    zip_code = request.args.get("areaCode")

    query = UserOrders.query.filter_by(zip_code=zip_code).first()

    basket = query.basket

    del basket[int(num)]

    # Postgres does not like the idea of updating lists, so we must save the data in another variable then append later.
    query.basket = []
    db.session.commit()

    query.basket = query.basket + basket
    db.session.commit()

    return {"fox": True}


@multiple_root_nodes()
def basket_list(request):
    zip_code = request.args.get("areaCode")
    query = UserOrders.query.filter_by(zip_code=zip_code).first()
    price = 0

    # Subtract the amount of indices in the list by 2 to get the amount we have to range over
    num = len(query.basket)
    data = []

    for i in range(num):
        price = float(query.basket[i]["price"].replace("$", "")) * float(
            query.basket[i]["qty"]
        ) + float(price)
        data.append(
            RepeatedElement(
                {
                    "basketNo": i,
                    "menuCode": 1,
                    "itemCode": 1,
                    "name": query.basket[i]["name"],
                    "price": query.basket[i]["price"],
                    "size": 1,
                    "isSoldout": 0,
                    "quantity": query.basket[i]["qty"],
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
                            "info": "Here so everything works!",
                            "code": 1,
                            "type": 1,
                            "name": "WiiLink",
                            "list": {
                                "item_one": {
                                    "name": "Item One",
                                    "menuCode": 1,
                                    "itemCode": 1,
                                    "image": 1,
                                    "isSoldout": 0,
                                    "info": "Here so everything works!",
                                    "price": "5.99",
                                }
                            },
                        }
                    },
                }
            )
        )

    # TODO: There is also "chargePrice" and "discountPrice".
    return {
        "basketPrice": price,
        "totalPrice": price,
        "Status": {"isOrder": 1, "messages": {"hey": "how are you?"}},
        "List": {"generic": data},
    }


@multiple_root_nodes()
def generate_auth_key(_):
    return {
        "authKey": str(uuid4()),
    }


@multiple_root_nodes()
def item_one(request):
    item_code = request.args.get("itemCode")
    queried_food = ItemList.query.filter_by(item_code=item_code).first()

    return {
        "price": queried_food.price,
        "optionList": {
            "testing": {
                "info": queried_food.description,
                "code": 1,
                "type": 1,
                "name": queried_food.name,
                "list": {"item_one": formulate_item(queried_food)},
            }
        },
    }


@multiple_root_nodes()
def item_list(request):
    menu_code = request.args.get("menuCode")
    queried_food = (
        ItemList.query.filter_by(menu_code=menu_code)
        .order_by(ItemList.item_code.asc())
        .all()
    )

    item_count = 0
    full_item_list = {}

    for index, current_item in enumerate(queried_food):
        item_count += 1

        current_item_list = {
            "name": current_item.name,
            "item": formulate_item(current_item),
        }

        # We need to populate sizes manually.
        current_item_list["item"]["sizeList"] = formulate_size_list(current_item)
        full_item_list.update({f"container{index}": current_item_list})

    return {"Count": item_count, "List": full_item_list}


@multiple_root_nodes()
def menu_list(request):
    shop_code = request.args.get("shopCode")
    query = (
        MenuList.query.filter_by(shop_code=shop_code)
        .order_by(MenuList.menu_code.asc())
        .all()
    )
    data = []

    for menu in query:
        data.append(
            RepeatedElement(
                {
                    "menuCode": menu.menu_code,
                    "linkTitle": menu.title,
                    "enabledLink": 1,
                    "name": menu.title,
                    "info": menu.info,
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
                }
            )
        )

    return {
        "response": {
            "menu": data,
            # Placeholder menu item so the rest can show
            "menu2": {
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


def formulate_size_list(item: ItemList) -> dict:
    """Formulates a complete size list for the given item."""

    # TODO: sizeList should be populated from actual data, instead of hardcoded.
    # For now, we will populate sizes with the generic size "Regular",
    # using the item's existing, configured properties.
    return {
        "itemCode": item.item_code,
        "name": item.name,
        "price": item.price,
        "info": item.description,
        "size": "Regular",
        "image": item.item_code,
        "isSoldout": 0,
    }


def formulate_item(item: ItemList) -> dict:
    """Generates a usable item description for the given item.

    Note that this only returns item metadata.
    You will need to provide size data separately."""

    return {
        "menuCode": item.menu_code,
        "itemCode": item.item_code,
        "name": item.name,
        "price": item.price,
        "info": item.description,
        "size": "Regular",
        "image": item.item_code,
        "isSoldout": 0,
    }


@multiple_root_nodes()
def shop_one(request):
    shop_code = request.args.get("shopCode")
    query = Shops.query.filter_by(shop_code=shop_code).first()

    # We'll synthesize recommended items using the first item of each
    # of this shop's menus.
    recommended_item_list = {}
    menus = MenuList.query.filter_by(shop_code=shop_code).all()
    for index, menu in enumerate(menus):
        # Every item within our recommendedItemList must be named
        # containerN, in an incremental fashion.
        container_name = f"container{index}"

        # Retrieve the first item of every menu.
        # TODO: This and the above MenuList query should be joined
        # for performance reasons.
        current_item = ItemList.query.filter_by(menu_code=menu.menu_code).first()
        item_contents = formulate_item(current_item)
        # We need to populate sizes manually.
        item_contents["sizeList"] = formulate_size_list(current_item)

        recommended_item_list[container_name] = item_contents

    return {
        "response": {
            "categoryCode": f"{query.category_code.value:02}",
            "address": query.address,
            "attention": "",
            "amenity": query.amenity,
            "menuListCode": 1,
            "activate": "on",
            "waitTime": 10,
            "timeorder": "y",
            "tel": query.phone,
            "yoyakuMinDate": 1,
            "yoyakuMaxDate": 30,
            "paymentList": {"athing": "Fox Card"},
            "interval": 30,
            "shopStatus": {
                "hours": {
                    "all": {
                        "message": query.message,
                    },
                    "today": {
                        "values": {
                            "hours": {
                                "start": "00:00:00",
                                "end": "24:59:59",
                                "holiday": "n",
                            }
                        }
                    },
                    "delivery": {
                        "values": {
                            "hours": {
                                "start": "00:00:00",
                                "end": "24:59:59",
                                "holiday": "n",
                            }
                        }
                    },
                },
                # Setting values to null will trigger the confirmation screen
                "selList": {},
                "holiday": "We're on holiday. Back soon!",
                "status": {
                    "isOpen": 1,
                },
            },
        },
        "recommendItemList": recommended_item_list,
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
        "container0": {"contents": eula_text},
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
                    "segment": "WiiLink",
                    "list": {"areaPlace": {"areaName": "WiiLink", "areaCode": 2}},
                },
            },
            "areaCount": 1,
        }

    if area_code == "2":
        # An area code of 0 is passed upon first search. All else is deterministic.
        # Assign the user a unique area code upon first launch of the channel
        zip_code = generate_random(11)

        data = UserOrders(
            zip_code=zip_code,
            basket=[],
        )

        db.session.add(data)
        db.session.commit()
        return {
            "areaList": {
                "place": {
                    "container0": "aaaa",
                    "segment": "WiiLink",
                    "list": {
                        "areaPlace": {
                            "areaName": "Reunion Tower",
                            "areaCode": zip_code,
                            "isNextArea": 0,
                            "display": 1,
                            "kanji1": "300",
                            "kanji2": "Reunion Tower",
                            "kanji3": "two",
                            "kanji4": "three",
                        }
                    },
                },
            },
            "areaCount": 1,
        }

    # If area_code isn't 2, something went terribly wrong
    return exceptions.NotFound()


def formulate_restaurant(category_id: CategoryTypes) -> dict:
    return {
        "LargeCategoryName": "Meal",
        "CategoryList": {
            "TestingCategory": {
                "CategoryCode": f"{category_id.value:02}",
                "ShopList": {"Shop": get_restaurant(category_id)},
            }
        },
    }


@multiple_root_nodes()
def category_list(request):
    zip_code = request.args.get("areaCode")
    query = UserOrders.query.filter_by(zip_code=zip_code).first()
    if not query:
        # The actual fix for this is for people to delete their save data and redo region setup.
        # I don't know why they won't just do that so here we are.
        query = UserOrders(
            zip_code=zip_code,
            basket=[],
        )

        db.session.add(query)
        db.session.commit()

    return {
        "response": {
            "Pizza": formulate_restaurant(CategoryTypes.Pizza),
            #   "Bento": formulate_restaurant(CategoryTypes.Bento_Box),
            #  "Sushi": formulate_restaurant(CategoryTypes.Sushi),
            # "Fish": formulate_restaurant(CategoryTypes.Fish),
            # "Seafood": formulate_restaurant(CategoryTypes.Seafood),
            # "American": formulate_restaurant(CategoryTypes.Western),
            # "Fast": formulate_restaurant(CategoryTypes.Fast_Food),
            # "Indian": formulate_restaurant(CategoryTypes.Curry),
            # "Party": formulate_restaurant(CategoryTypes.Party_Food),
            "Drinks": formulate_restaurant(CategoryTypes.Others),
            "Other": formulate_restaurant(CategoryTypes.Test),
            "Placeholder": formulate_restaurant(CategoryTypes.Others),
        }
    }


@multiple_root_nodes()
def basket_add(request):
    zip_code = request.form.get("areaCode")
    item_code = request.form.get("itemCode")
    qty = request.form.get("quantity")
    auth_key = request.form.get("authKey")

    query = UserOrders.query.filter_by(zip_code=zip_code).first()
    queried_food = ItemList.query.filter_by(item_code=item_code).first()

    # Check if the user has a stale basket
    if query.auth_key != auth_key:
        query.auth_key = auth_key
        query.basket = []
        db.session.commit()

    # Append data to the database
    # Temporary hack to allow basket migration.
    order: list = query.basket or []
    basket = order + [
        {"name": queried_food.name, "price": queried_food.price, "qty": qty}
    ]

    query.basket = basket
    db.session.commit()

    return {"sketch": True}


@multiple_root_nodes()
def validate_condition(_):
    return {}


@response()
def order_done(request):
    """Now that the order is complete, remove our basket from the database."""
    auth_key = request.form.get("authKey")
    query = UserOrders.query.filter_by(auth_key=auth_key).first()

    # We require this specific format.
    # With "orderDay", this handles the year [0:4], month [4:6], and day [6:8].
    # Meanwhile, the channel only parses "hour" at [8:10], and minute at [10:12].
    current_time = datetime.utcnow().strftime("%Y%m%d%H%S")

    query.basket = []
    query.auth_key = None
    db.session.commit()
    return {
        "Message": {"contents": "Thank you! Your order has been placed."},
        "order_id": 17,
        "orderDay": current_time,
        "hashKey": "Testing: 1, 2, 3",
        "hour": current_time,
    }
