from flask import request, redirect, url_for, render_template, flash, session

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
        return render_template("profile.html", username=username)
    else:
        flash("You need to log in first", "danger")
        return redirect(url_for("users.login"))