from food import app
from flask import render_template, send_from_directory, redirect, url_for, flash
from flask_oidc import OpenIDConnect

import config

oidc = OpenIDConnect(app)

@app.context_processor
def inject_oidc():
    return dict(oidc=oidc)

@app.route("/thepantry")
@app.route("/thepantry/")
def root():
    return redirect(url_for("login"))


@app.route("/thepantry/login")
def login():
    if oidc.user_loggedin:
        return redirect(url_for("admin"))

    return render_template("login.html")


@app.route("/thepantry/admin")
@oidc.require_login
def admin():
    return render_template("pantry.html")

@app.route("/thepantry/logout")
@oidc.require_login
def logout():
    oidc.logout()
    response = redirect(config.oidc_logout_url)
    response.set_cookie("session", expires=0)
    return response


@app.route("/thepantry/common.css")
def common_css():
    return send_from_directory("templates", "common.css")
