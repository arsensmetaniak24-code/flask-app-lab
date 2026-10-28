from flask import request, redirect, url_for, render_template, flash, session
from functools import wraps

from . import users_bp

users = {
    "admin": "password",
    "arsen": "arsenSecret"
}

@users_bp.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age")

    return render_template('hi.html', name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greeting", name="admin", age="42", _external=True)
    return redirect(to_url)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Enter username and password", "danger")
        return redirect(url_for("users.login"))

    if users.get(username) == password:
        session["username"] = username
        flash("Welcome, " + username + "!", "success")
        return redirect(url_for("users.profile"))
    else:
        flash("Wrong username or password", "danger")
        return redirect(url_for("users.login"))

@users_bp.route("/profile", methods=["GET"])
def profile():
    username = session.get("username")
    if username:
        return render_template("profile.html",
                               username=username,
                               cookies=request.cookies,
                               theme=request.cookies.get("theme", "dark"))
    else:
        flash("You need to log in first", "danger")
        return redirect(url_for("users.login"))

@users_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("username", None)
    flash("You have been logged out", "success")
    return redirect(url_for("users.login"))

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            flash("You must be logged in to access this page", "danger")
            return redirect(url_for("users.login"))
        return view(*args, **kwargs)
    return wrapper

@users_bp.route("/cookies/add", methods=["POST"])
@login_required
def add_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    max_age = request.form.get("max_age")

    if max_age:
        try:
            max_age = int(max_age)
        except ValueError:
            flash("Invalid max age", "danger")
            return redirect(url_for("users.profile"))
    else:
        max_age = None

    if not key or not value:
        flash("Enter key and value", "danger")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie(key, value, max_age=max_age)

    flash("Cookie added", "success")

    return response

@users_bp.route("/cookies/delete", methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key")
    if not key:
        flash("Enter key", "warning")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash("Cookie not found", "warning")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.delete_cookie(key)
    flash("Cookie deleted", "success")
    return response

@users_bp.route("/cookies/delete-all", methods=["POST"])
@login_required
def delete_all_cookies():
    response = redirect(url_for("users.profile"))
    for key in request.cookies:
        if key in ["session", "theme"]:
            continue
        response.delete_cookie(key)
    flash("All cookies deleted", "success")
    return response


@users_bp.route("/theme/<scheme>", methods=["GET"])
@login_required
def change_theme(scheme):
    if scheme not in ["light", "dark"]:
        flash("Invalid theme", "danger")
        return redirect(url_for("users.profile"))

    response = redirect(url_for("users.profile"))
    response.set_cookie("theme", scheme, max_age=60*60*24*365)
    flash("Theme changed", "success")
    return response