import shutil

from food import app, db
from flask_login import login_required
from thepantry.forms import FoodTypes, RestaurantEditForm, RestaurantAddForm
from flask import render_template, url_for, redirect, send_from_directory
from werkzeug import exceptions
from models import Shops, CategoryTypes, ItemList, MenuList
from thepantry.encodemii import save_restaurant_logo
from thepantry.operations import manage_delete_item
import os

@app.route("/thepantry/resturantrequests", methods=["GET", "POST"])
@login_required
def list_resturantrequests():
    shoprequests = ShopRequests.query.all()
    return render_template(
        "requests.html", shoprequests=shoprequests, type_length=len(shoprequests), type_max_count=64
    )

@app.route("/theunderground/resturantrequests/<resturantrequest_id>/remove", methods=["GET", "POST"])
@login_required
def remove_resturantrequest(resturantrequest_id):
    def drop_resturantrequest():
        db.session.delete(ShopRequests.query.filter_by(id=resturantrequest_id).first())
        db.session.commit()
        return redirect(url_for("list_resturantrequests"))

    return manage_delete_item(resturantrequest_id, "shoprequests", drop_resturantrequest)



@app.route("/thepantry/restaurants", methods=["GET", "POST"])
@login_required
def select_food_type():
    form = FoodTypes()
    if form.validate_on_submit():
        value = form.food.data
        return redirect(url_for("view_restaurants", category=value))

    return render_template("select_food_type.html", form=form)


@app.route("/thepantry/restaurants/<category>")
@login_required
def view_restaurants(category):
    restaurants = (
        Shops.query.filter_by(category_code=CategoryTypes(int(category)).name)
        .order_by(Shops.shop_code.asc())
        .paginate(1, 15, error_out=False)
    )

    return render_template(
        "restaurants_list.html",
        stores=restaurants,
        type_length=restaurants.total,
        # TODO: Find the maximum amount of restaurants possible
        type_max_count=64,
    )


@app.route("/thepantry/categories/add", methods=["GET", "POST"])
@login_required
def add_restaurant():
    form = RestaurantAddForm()

    if form.validate_on_submit():
        new_restaurant = Shops(
            name=form.restaurant_name.data,
            category_code=form.food_type.data,
            description=form.description.data,
            wait_time=form.wait_time.data,
            address=form.address.data,
            amenity=form.amenity.data,
            phone=form.phone.data,
            message=form.message.data,
        )

        # Add to retrieve the category ID.
        db.session.add(new_restaurant)
        db.session.commit()

        # With this ID, write the thumbnail.
        save_restaurant_logo(form.logo.data.read(), new_restaurant.shop_code)
        return redirect(url_for("select_food_type"))

    return render_template("restaurant_add.html", form=form)


@app.route("/thepantry/categories/<restaurant_id>/edit", methods=["GET", "POST"])
@login_required
def edit_restaurant(restaurant_id):
    form = RestaurantEditForm()

    # Populate data
    current_restaurant = Shops.query.filter_by(shop_code=restaurant_id).first()
    if not current_restaurant:
        return exceptions.NotFound()

    if form.validate_on_submit():
        current_restaurant.name = form.restaurant_name.data
        current_restaurant.description = form.description.data
        current_restaurant.wait_time = form.wait_time.data
        current_restaurant.address = form.address.data
        current_restaurant.amenity = form.amenity.data
        current_restaurant.phone = form.phone.data
        current_restaurant.message = form.message.data
        db.session.commit()

        # Check if we have a new thumbnail.
        if form.logo.data:
            save_restaurant_logo(form.logo.data.read(), restaurant_id)

        return redirect(url_for("select_food_type"))
    else:
        # Populate the current name.
        # category_add.html below will populate the current thumbnail.
        form.restaurant_name.data = current_restaurant.name
        form.description.data = current_restaurant.description
        form.wait_time.data = current_restaurant.wait_time
        form.address.data = current_restaurant.address
        form.amenity.data = current_restaurant.amenity
        form.phone.data = current_restaurant.phone
        form.message.data = current_restaurant.message

    return render_template("restaurant_edit.html", store=current_restaurant, form=form)


@app.route("/thepantry/categories/<restaurant_id>/delete", methods=["GET", "POST"])
@login_required
def remove_restaurant(restaurant_id):
    def drop_restaurant():
        # Since we are deleting the entire restaurant, we will need to delete food items.
        ItemList.query.filter(MenuList.shop_code == restaurant_id).filter(
            MenuList.menu_code == ItemList.menu_code
        ).delete(synchronize_session=False)
        db.session.commit()

        # Next, delete the menus itself.
        MenuList.query.filter_by(shop_code=restaurant_id).delete()
        db.session.commit()

        # As there are no more menu items referencing this shop, delete it.
        Shops.query.filter_by(shop_code=restaurant_id).delete()
        db.session.commit()

        # Lastly, remove assets on disk, where possible.
        if os.path.exists(f"./images/{restaurant_id}.jpg"):
            os.remove(f"./images/{restaurant_id}.jpg")

        if os.path.isdir(f"./images/{restaurant_id}"):
            shutil.rmtree(f"./images/{restaurant_id}")

        return redirect(url_for("select_food_type"))

    return manage_delete_item(restaurant_id, "restaurant", drop_restaurant)


@app.route("/thepantry/restaurants/<shop_code>/logo.jpg")
@login_required
def get_restaurant_logo(shop_code):
    return send_from_directory("./images/", f"{shop_code}.jpg")
