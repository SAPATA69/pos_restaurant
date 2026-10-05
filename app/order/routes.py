from decimal import Decimal
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.auth.permissions import roles_required
from app.models import MenuItem, Order, OrderItem, Table

order_bp = Blueprint("order", __name__, url_prefix="/order")

@order_bp.route("/tables")
@login_required
@roles_required("admin", "staff")
def select_table():
    return render_template("order/tables.html", tables=Table.query.order_by(Table.table_number).all())

@order_bp.route("/takeaway")
@login_required
@roles_required("admin", "staff")
def takeaway():
    order = Order.query.filter_by(table_id=None, order_type="takeaway", status="open").first()
    if not order:
        order = Order(user_id=current_user.id, order_type="takeaway"); db.session.add(order); db.session.commit()
    return redirect(url_for("order.take_order", order_id=order.id))

@order_bp.route("/table/<int:table_id>")
@login_required
@roles_required("admin", "staff")
def open_table(table_id):
    table = Table.query.get_or_404(table_id)
    order = Order.query.filter_by(table_id=table.id, status="open").first()
    if not order:
        order = Order(table_id=table.id, user_id=current_user.id, order_type="dine_in"); table.status = "occupied"; db.session.add(order); db.session.commit()
    return redirect(url_for("order.take_order", order_id=order.id))

@order_bp.route("/<int:order_id>", methods=["GET", "POST"])
@login_required
@roles_required("admin", "staff")
def take_order(order_id):
    order = Order.query.get_or_404(order_id)
    if request.method == "POST":
        menu_item = MenuItem.query.get_or_404(int(request.form["menu_item_id"]))
        if not menu_item.is_available: flash("เมนูนี้หมดชั่วคราว", "warning"); return redirect(url_for("order.take_order", order_id=order.id))
        option_ids = request.form.getlist("option_ids")
        selected = [option for option in menu_item.options if str(option.id) in option_ids and option.is_available]
        quantity = max(1, int(request.form.get("quantity", 1)))
        item = OrderItem(order=order, menu_item=menu_item, quantity=quantity, unit_price=menu_item.price, option_text=", ".join(o.name for o in selected) or None, option_total=sum((o.price for o in selected), Decimal("0")), note=request.form.get("note", "").strip() or None)
        db.session.add(item); order.recalculate_total(); db.session.commit(); flash("เพิ่มรายการอาหารแล้ว", "success")
        return redirect(url_for("order.take_order", order_id=order.id))
    return render_template("order/take_order.html", order=order, menu_items=MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category, MenuItem.name).all())

@order_bp.route("/<int:order_id>/send", methods=["POST"])
@login_required
@roles_required("admin", "staff")
def send_to_kitchen(order_id):
    order = Order.query.get_or_404(order_id)
    if not order.items: flash("กรุณาเพิ่มรายการอาหารก่อนส่งครัว", "warning")
    else: flash("ส่งออเดอร์เข้าคิวครัวแล้ว", "success")
    return redirect(url_for("order.take_order", order_id=order.id))
