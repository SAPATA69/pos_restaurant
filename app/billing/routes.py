from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.models import Order, Table

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")


@billing_bp.route("/<int:order_id>")
@login_required
def bill(order_id):
    order = Order.query.get_or_404(order_id)
    total = sum(item.menu_item.price * item.quantity for item in order.items)
    order.total_amount = total
    return render_template("billing/bill.html", order=order, total=total)


@billing_bp.route("/<int:order_id>/pay", methods=["POST"])
@login_required
def pay(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = "paid"
    order.table.status = "available"
    db.session.commit()
    return redirect(url_for("order.select_table"))
