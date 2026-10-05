from decimal import Decimal, InvalidOperation
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.auth.permissions import roles_required
from app.models import Order, Payment

billing_bp = Blueprint("billing", __name__, url_prefix="/billing")

@billing_bp.route("/<int:order_id>")
@login_required
@roles_required("admin", "staff")
def bill(order_id):
    order = Order.query.get_or_404(order_id); order.recalculate_total(); db.session.commit()
    return render_template("billing/bill.html", order=order, total=order.total_amount)

@billing_bp.route("/<int:order_id>/pay", methods=["POST"])
@login_required
@roles_required("admin", "staff")
def pay(order_id):
    order = Order.query.get_or_404(order_id); method = request.form.get("method", "cash")
    try: received = Decimal(request.form.get("received_amount") or str(order.total_amount))
    except InvalidOperation: flash("จำนวนเงินไม่ถูกต้อง", "danger"); return redirect(url_for("billing.bill", order_id=order.id))
    if method == "cash" and received < order.total_amount: flash("จำนวนเงินสดไม่พอ", "danger"); return redirect(url_for("billing.bill", order_id=order.id))
    change = received - order.total_amount if method == "cash" else Decimal("0")
    order.status = "paid"
    if order.table: order.table.status = "available"
    db.session.add(Payment(order=order, method=method, amount=order.total_amount, received_amount=received, change_amount=change))
    db.session.commit(); return redirect(url_for("billing.receipt", order_id=order.id))

@billing_bp.route("/<int:order_id>/receipt")
@login_required
def receipt(order_id):
    return render_template("billing/receipt.html", order=Order.query.get_or_404(order_id))
