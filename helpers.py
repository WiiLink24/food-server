import base64
import functools
from lxml import etree

from models import Shops


def generate_response_dict(passed_dict) -> dict:
    passed_dict["apiStatus"] = {"code": 0}
    passed_dict["version"] = 1

    return passed_dict


def response():
    def decorator(func):
        @functools.wraps(func)
        def serialization_wrapper(*args, **kwargs):
            returned_value = func(*args, **kwargs)

            # Ensure we are truly dealing with a dictionary.
            if isinstance(returned_value, dict):
                # Insert common elements.
                returned_value = generate_response_dict(returned_value)

                # Serialize to an ETree.
                elements = dict_to_etree("response", returned_value)

                # We now must convert from ETree to actual XML we can respond with.
                return etree.tostring(
                    elements,
                    encoding="shift-jis",
                    xml_declaration=False,
                    pretty_print=True,
                )
            else:
                # We only apply XML operations to dicts.
                return returned_value

        return serialization_wrapper

    return decorator


def multiple_root_nodes():
    """
    Nintendo makes questionable decisions. This is a fact.
    Some of them one may consider somewhat justified, based on development
    time and constraint.

    Consider the following C pseudocode:

    int index = 0;
    int count = GetChildNodeCount(responseNode);
    while (index < count - 1) {
      // [...]
    }

    Nintendo loops through the count of all response codes.
    As having apiStatus -> code and version normally
    would mean response has a child count of 2 and other restaurants,
    they violate every XML standard known to humankind and parse it separately.

    It would not hurt them to have put the data inside of a separate node.
    It would not hurt them to subtract 2 should they require "response" for unknown standards.
    Even worse, this is Wii-specific, as none of their mobile applications
    (iPhone OS 3.1 or Android 2.2, earliest found) rely on any of this functionality.
    Yet, here we are.

    We append such manually, as they use this syntax in multiple locations.
    """

    def decorator(func):
        @functools.wraps(func)
        def serialization_wrapper(*args, **kwargs):
            returned_value = func(*args, **kwargs)

            # Only operate on dictionaries.
            if isinstance(returned_value, dict):
                # Insert common elements.
                returned_value = generate_response_dict(returned_value)

                working_response = b""

                for root_name, children in returned_value.items():
                    elements = dict_to_etree(root_name, children)

                    # Convert to bytes.
                    working_response += etree.tostring(
                        elements,
                        encoding="shift-jis",
                        xml_declaration=False,
                        pretty_print=True,
                    )

                # We now have all root nodes.
                return working_response
            else:
                return returned_value

        return serialization_wrapper

    return decorator


def dict_to_etree(tag_name: str, d: dict) -> etree.Element:
    """ Derived from https://stackoverflow.com/a/10076823. """

    def _to_etree(d, root):
        if d is None:
            pass
        elif isinstance(d, bool):
            # We can only accept 0 or 1 as Nintendo's "boolean" types.
            root.text = etree.CDATA("1" if d else "0")
        elif isinstance(d, int):
            root.text = etree.CDATA(f"{d}")
        elif isinstance(d, Kana):
            value = etree.SubElement(root, "kana")
            value.text = d.contents
        elif isinstance(d, Yomi):
            value = etree.SubElement(root, "yomi")
            value.text = d.contents
        elif isinstance(d, str):
            root.text = etree.CDATA(d)
        elif isinstance(d, bytes):
            # We're going to assume this needs to be Base64 encoded.
            root.text = etree.CDATA(base64.b64encode(d))
        elif isinstance(d, tuple) or isinstance(d, list):
            # As we're backed by K/V notation,a tuple or a list is useless.
            # It should only contain our special
            # RepeatedKeys and RepeatedNodes types.
            should_delete = False
            for v in d:
                if isinstance(v, RepeatedElement):
                    # We'd like to duplicate this specific node in its parent.
                    # Now we need to obtain such.
                    parent_elem = root.getparent()
                    # Create a new sub-element in the parent with the current
                    # element's name.
                    new_elem = etree.SubElement(parent_elem, root.tag)

                    _to_etree(v.contents, new_elem)
                    should_delete = True
                elif isinstance(v, RepeatedKey):
                    # We'd like to duplicate keys within this node.
                    # Retain the parent and operate on the dict.
                    _to_etree(v.contents, root)
                else:
                    raise ValueError(f"invalid type {type(v).__name__} specified")
            if should_delete:
                # Delete ourselves once added as other repeated elements have replaced us.
                root.getparent().remove(root)
        elif isinstance(d, dict):
            for k, v in d.items():
                assert isinstance(k, str)
                _to_etree(v, etree.SubElement(root, k))
        else:
            assert d == "invalid type", (type(d), d)

    node = etree.Element(tag_name)
    _to_etree(d, node)
    return node


class RepeatedKey:
    """This class is intended to clarify disambiguation when converting from a dict.
    Its specific behavior is to repeat its keys within a parent node.

    For example:
    <Parent>
        <key>value</key>
        <second>value</second>
        <key>value</key>
        <second>value</second>
    </Parent>
    """

    contents = {}

    def __init__(self, passed_dict):
        if not isinstance(passed_dict, dict):
            raise ValueError("Please only pass dicts to RepeatedKey.")
        self.contents = passed_dict


class RepeatedElement:
    """This class is intended to clarify disambiguation when converting from a dict.
    Its specific behavior is to allow repeating an element against its parent.

    For example:
    <Parent>
        <key>value</key>
        <second>value</second>
    </Parent>
    <Parent>
        <key>value</key>
        <second>value</second>
    </Parent>
    """

    contents = {}

    def __init__(self, passed_dict):
        if not isinstance(passed_dict, dict):
            raise ValueError("Please only pass dicts to RepeatedElement.")
        self.contents = passed_dict


class Kana:
    """The Kana class is intended to represent kana. By default, the Demae Channel's parser
    strips non-ASCII characters. When within a kana tag, this process does not occur."""

    contents = ""

    def __init__(self, contents):
        if not isinstance(contents, str):
            raise ValueError("Please only pass strings to Kana.")
        self.contents = contents


class Yomi:
    """The Yomi class is intended to represent kanji. By default, the Demae Channel's parser
    strips non-ASCII characters. When within a kana tag, this process does not occur."""

    def __init__(self, contents):
        if not isinstance(contents, str):
            raise ValueError("Please only pass strings to Yomi.")
        self.contents = contents


def get_restaurant(categoryid):
    """This function grabs basic restaurant information recursively, so we can have
    multiple restaurants without having to insert it manually in responses.py"""
    # All category names and values: https://gist.github.com/SketchMaster2001/42172c8b00075b4b827fa2f78a9eb9e1
    queried_categories = Shops.query.filter_by(category_code=categoryid).all()
    results = []

    for i, restaurant in enumerate(queried_categories):
        # Items must be indexed by 1.
        results.append(
            RepeatedElement(
                {
                    "shopCode": restaurant.shop_code,
                    "homeCode": restaurant.restaurant_id,
                    "name": restaurant.name,
                    "catchphrase": restaurant.description,
                    "minPrice": 1,
                    "yoyaku": 1,
                    "activate": "on",
                    "waitTime": restaurant.wait_time,
                    "paymentList": {"athing": "Fox Card"},
                    "shopStatus": {
                        "status": {
                            "isOpen": restaurant.open,
                        }
                    },
                }
            )
        )

    return results
