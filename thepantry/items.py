from food import app, db
from models import ItemList
from flask import render_template, send_from_directory, redirect, url_for
from flask_login import login_required
from werkzeug import exceptions
from thepantry.forms import ItemEditForm, ItemAddForm
from thepantry.encodemii import save_food_image
import os
from thepantry.operations import manage_delete_item


@app.route("/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/items")
@login_required
def list_food_items(restaurant_id, menu_code):
    items = (
        ItemList.query.filter_by(menu_code=int(menu_code))
        .order_by(ItemList.item_code.asc())
        .paginate(1, 15, error_out=False)
    )

    return render_template(
        "item_list.html",
        items=items,
        type_length=items.total,
        type_max_count=64,
        restaurant_id=restaurant_id,
        menu_code=menu_code,
    )


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/items/<item_code>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_item(restaurant_id, menu_code, item_code):
    form = ItemEditForm()

    current_item = ItemList.query.filter_by(item_code=item_code).first()
    if not current_item:
        return exceptions.NotFound()

    if form.validate_on_submit():
        current_item.name = form.name.data
        current_item.description = form.description.data
        current_item.price = form.price.data
        db.session.commit()

        if form.image.data:
            save_food_image(form.image.data.read(), restaurant_id, item_code)

        return redirect(
            url_for(
                "list_food_items",
                restaurant_id=restaurant_id,
                menu_code=current_item.menu_code,
            )
        )
    else:
        # Populate the current name.
        # item_edit.html below will populate the current thumbnail.
        form.name.data = current_item.name
        form.description.data = current_item.description
        form.price.data = current_item.price

    return render_template(
        "item_edit.html", item=current_item, form=form, restaurant_id=restaurant_id
    )


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/items/add",
    methods=["GET", "POST"],
)
@login_required
def add_item(restaurant_id, menu_code):
    form = ItemAddForm()

    if form.validate_on_submit():
        new_menu = ItemList(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            menu_code=menu_code,
        )

        # Commit to the database
        db.session.add(new_menu)
        db.session.commit()

        # Now that it successfully saved to the db, we can save to disk
        save_food_image(form.image.data.read(), restaurant_id, new_menu.item_code)
        return redirect(
            url_for("list_food_items", restaurant_id=restaurant_id, menu_code=menu_code)
        )

    return render_template("item_add.html", form=form)


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/items/<item_code>/delete",
    methods=["GET", "POST"],
)
@login_required
def remove_item(restaurant_id, menu_code, item_code):
    def drop_item():
        item = ItemList.query.filter_by(item_code=item_code).first()
        db.session.delete(item)

        db.session.commit()
        os.remove(f"./images/{restaurant_id}/{item_code}.jpg")

        return redirect(
            url_for("list_food_items", restaurant_id=restaurant_id, menu_code=menu_code)
        )

    return manage_delete_item(restaurant_id, "item", drop_item)


@app.route("/thepantry/restaurants/items/<restaurant_id>/<item_code>.jpg")
@login_required
def get_food_image(restaurant_id, item_code):
    return send_from_directory(f"./images/{restaurant_id}/", item_code + ".jpg")
