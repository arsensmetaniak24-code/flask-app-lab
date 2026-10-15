from flask import Blueprint, request, redirect, url_for, render_template

from .. import app

@app.route("/hi/<string:name>")
def greeting(name):
    name = name.upper()
    age = request.args.get("age")

    return render_template('hi.html', name=name, age=age)

@app.route("/admin")
def admin():
    to_url = url_for("greeting", name="admin", age="42", _external=True)
    return redirect(to_url)