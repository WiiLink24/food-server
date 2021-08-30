from food import app, db
from models import MenuList, Shops, ItemList
from flask import render_template, redirect, url_for
from flask_login import login_required
from thepantry.forms import MenuEditForm, MenuAddForm
from werkzeug import exceptions
import os
from thepantry.operations import manage_delete_item


@app.route("/thepantry/restaurants/<restaurant_id>/menus")
@login_required
def list_menus(restaurant_id):
    menus = (
        MenuList.query.filter_by(shop_code=int(restaurant_id))
        .order_by(MenuList.menu_code.asc())
        .paginate(1, 15, error_out=False)
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
@login_required
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
@login_required
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

        return redirect(url_for("list_menus", restaurant_id=restaurant_id))

    return render_template(
        "menu_add.html", form=form, current_restaurant=current_restaurant
    )


@app.route(
    "/thepantry/restaurants/<restaurant_id>/menus/<menu_code>/delete",
    methods=["GET", "POST"],
)
@login_required
def remove_menu(restaurant_id, menu_code):
    def drop_menu():
        # Delete the menu and it's children
        items = ItemList.query.filter_by(menu_code=menu_code).all()
        for item in items:
            db.session.delete(item)

        menu = MenuList.query.filter_by(menu_code=menu_code).first()
        db.session.delete(menu)

        db.session.commit()
        os.unlink(f"./images/{restaurant_id}")

        return redirect(url_for("list_menus", restaurant_id=restaurant_id))

    return manage_delete_item(restaurant_id, "menu", drop_menu())
