import io
from PIL import Image, ImageFile


def save_restaurant_logo(in_bytes: bytes, restaurant_id: int):
    logo_data = generic_encode(in_bytes, 160, 160)
    logo = open(f"./images/{restaurant_id}.jpg", "wb")
    logo.write(logo_data)
    logo.close()


def save_food_image(in_bytes: bytes, restaurant_id: int, item_code: int):
    image_data = generic_encode(in_bytes, 160, 160)
    image = open(f"./images/{restaurant_id}/{item_code}.jpg", "wb")
    image.write(image_data)
    image.close()


def generic_encode(in_bytes: bytes, w: int, h: int) -> bytes:
    """Encodes an image to a format suitable for the Wii."""
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open(io.BytesIO(in_bytes))

    # If we have an alpha channel, it must be removed.
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")

    im = im.resize((w, h))

    result = io.BytesIO()
    # These defaults are required for the Wii to read an JPEG.
    im.save(result, "jpeg", subsampling="4:2:0", progressive=False)

    return result.getvalue()
