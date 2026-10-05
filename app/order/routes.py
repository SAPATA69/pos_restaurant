from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Table, Order, OrderItem, MenuItem

order_bp = Blueprint("order", __name__, url_prefix="/order")


@order_bp.route("/tables")
@login_required
def select_table():
    tables = Table.query.all()
    return render_template("order/tables.html", tables=tables)


@order_bp.route("/table/<int:table_id>", methods=["GET", "POST"])
@login_required
def take_order(table_id):
    table = Table.query.get_or_404(table_id)
    order = Order.query.filter_by(table_id=table_id, status="open").first()
    if not order:
        order = Order(table_id=table_id, user_id=current_user.id)
        table.status = "occupied"
        db.session.add(order)
        db.session.commit()

    if request.method == "POST":
        menu_item_id = request.form.get("menu_item_id")
        quantity = int(request.form.get("quantity", 1))
        oi = OrderItem(order_id=order.id, menu_item_id=menu_item_id, quantity=quantity)
        db.session.add(oi)
        db.session.commit()
        return redirect(url_for("order.take_order", table_id=table_id))

    menu_items = MenuItem.query.filter_by(is_available=True).all()
    return render_template("order/take_order.html", table=table, order=order, menu_items=menu_items)
