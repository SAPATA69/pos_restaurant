from decimal import Decimal, InvalidOperation
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.auth.permissions import roles_required
from app.models import MenuItem, MenuOption

menu_bp = Blueprint("menu", __name__, url_prefix="/menu")

@menu_bp.route("/")
@login_required
def list_items():
    return render_template("menu/list.html", items=MenuItem.query.order_by(MenuItem.category, MenuItem.name).all())

@menu_bp.route("/add", methods=["GET", "POST"])
@login_required
@roles_required("admin")
def add_item():
    if request.method == "POST":
        try: price = Decimal(request.form.get("price", "0"))
        except InvalidOperation: flash("ราคาต้องเป็นตัวเลข", "danger"); return render_template("menu/add.html")
        item = MenuItem(name=request.form.get("name", "").strip(), price=price, category=request.form.get("category", "ทั่วไป").strip() or "ทั่วไป")
        options = [x.strip() for x in request.form.get("options", "").split(",") if x.strip()]
        item.options = [MenuOption(name=x) for x in options]
        db.session.add(item); db.session.commit(); flash("เพิ่มเมนูแล้ว", "success")
        return redirect(url_for("menu.list_items"))
    return render_template("menu/add.html")

@menu_bp.route("/<int:item_id>/toggle", methods=["POST"])
@login_required
@roles_required("admin")
def toggle(item_id):
    item = MenuItem.query.get_or_404(item_id); item.is_available = not item.is_available
    db.session.commit(); return redirect(url_for("menu.list_items"))
