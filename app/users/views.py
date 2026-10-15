from flask import request, redirect, url_for, render_template

from .. import app
from . import users_bp

@users_bp.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age")

    return render_template('hi.html', name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greeting", name="admin", age="42", _external=True)
    return redirect(to_url)