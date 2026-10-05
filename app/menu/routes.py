from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import MenuItem

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")


@menu_bp.route("/")
@login_required
def list_items():
    items = MenuItem.query.all()
    return render_template("menu/list.html", items=items)


@menu_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    if request.method == "POST":
        item = MenuItem(
            name=request.form.get("name"),
            price=request.form.get("price"),
            category=request.form.get("category"),
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("menu.list_items"))
    return render_template("menu/add.html")
