from food import app, db
from models import MenuList, Shops, ItemList
from flask import render_template, redirect, url_for
from thepantry.forms import MenuEditForm, MenuAddForm
from werkzeug import exceptions
import os
from thepantry.operations import manage_delete_item
from thepantry.admin import oidc


@app.route("/thepantry/restaurants/<restaurant_id>/menus")
@oidc.require_login
def list_menus(restaurant_id):
    menus = (
        MenuList.query.filter_by(shop_code=int(restaurant_id))
        .order_by(MenuList.menu_code.asc())
        .paginate(page=1, per_page=15, error_out=False)
    )

    return render_template(
        "menu_list.html",
        menus=menus,
        type_length=menus.total,
        type_max_count=64,
        restaurant_id=restaurant_id,
    )


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_id>/edit",
    methods=["GET", "POST"],
)
@oidc.require_login
def edit_menu(restaurant_id, menu_id):
    form = MenuEditForm()

    current_menu = MenuList.query.filter_by(menu_code=menu_id).first()
    if not current_menu:
        return exceptions.NotFound()

    if form.validate_on_submit():
        current_menu.title = form.menu_name.data
        current_menu.info = form.info.data
        db.session.commit()

        return redirect(url_for("list_menus", restaurant_id=restaurant_id))
    else:
        # Populate the current name.
        # category_add.html below will populate the current thumbnail.
        form.menu_name.data = current_menu.title
        form.info.data = current_menu.info

    return render_template("menu_edit.html", store=current_menu, form=form)


@app.route("/thepantry/restaurants/<restaurant_id>/menus/add", methods=["GET", "POST"])
@oidc.require_login
def add_menu(restaurant_id):
    form = MenuAddForm()

    # We will query the Shops table just so we can tell the user what restaurant they are adding a menu for.
    # I want no ambiguity on what the user is adding for.
    current_restaurant = Shops.query.filter_by(shop_code=restaurant_id).first()
    if not current_restaurant:
        # This should also never happen but you never know
        return exceptions.NotFound()

    if form.validate_on_submit():
        new_menu = MenuList(
            title=form.menu_name.data,
            info=form.info.data,
            shop_code=restaurant_id,
        )

        db.session.add(new_menu)
        db.session.commit()

        if not os.path.isdir(f"./images/{restaurant_id}"):
            os.mkdir(f"./images/{restaurant_id}")

        return redirect(url_for("list_menus", restaurant_id=restaurant_id))

    return render_template(
        "menu_add.html", form=form, current_restaurant=current_restaurant
    )


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/delete",
    methods=["GET", "POST"],
)
@oidc.require_login
def remove_menu(restaurant_id, menu_code):
    def drop_menu():
        # Delete the menu and it's children
        items = ItemList.query.filter_by(menu_code=menu_code).all()
        for item in items:
            # Remove this item's image.
            item_image = f"./images/{restaurant_id}/{item.item_code}.jpg"
            if os.path.exists(item_image):
                os.remove(item_image)

            db.session.delete(item)

        menu = MenuList.query.filter_by(menu_code=menu_code).first()
        db.session.delete(menu)

        db.session.commit()

        return redirect(url_for("list_menus", restaurant_id=restaurant_id))

    return manage_delete_item(restaurant_id, "menu", drop_menu)
