from datetime import date, datetime, time, timedelta
from decimal import Decimal
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.auth.permissions import roles_required
from app.models import MenuItem, Order, OrderItem, Payment

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")

def date_range(start_text, end_text):
    today = date.today()
    try: start = datetime.strptime(start_text, "%Y-%m-%d").date() if start_text else today
    except ValueError: start = today
    try: end = datetime.strptime(end_text, "%Y-%m-%d").date() if end_text else start
    except ValueError: end = start
    if end < start: start, end = end, start
    return datetime.combine(start, time.min), datetime.combine(end, time.max), start.isoformat(), end.isoformat()

def paid_query(start_dt, end_dt):
    return Payment.query.join(Order).filter(Payment.paid_at >= start_dt, Payment.paid_at <= end_dt, Order.status == "paid")

@reports_bp.route("/")
@login_required
@roles_required("admin", "staff")
def sales_dashboard():
    start_dt, end_dt, start, end = date_range(request.args.get("start", ""), request.args.get("end", ""))
    payments = paid_query(start_dt, end_dt).order_by(Payment.paid_at.desc()).all()
    total = sum((payment.amount for payment in payments), Decimal("0.00"))
    by_method = db.session.query(Payment.method, func.sum(Payment.amount), func.count(Payment.id)).join(Order).filter(Payment.paid_at >= start_dt, Payment.paid_at <= end_dt, Order.status == "paid").group_by(Payment.method).all()
    orders = [payment.order for payment in payments]
    return render_template("reports/sales.html", payments=payments, total=total, order_count=len(orders), by_method=by_method, start=start, end=end)

@reports_bp.route("/payments")
@login_required
@roles_required("admin", "staff")
def payment_history():
    start_dt, end_dt, start, end = date_range(request.args.get("start", ""), request.args.get("end", ""))
    payments = paid_query(start_dt, end_dt).order_by(Payment.paid_at.desc()).all()
    return render_template("reports/payments.html", payments=payments, start=start, end=end)

@reports_bp.route("/best-sellers")
@login_required
@roles_required("admin", "staff")
def best_sellers():
    start_dt, end_dt, start, end = date_range(request.args.get("start", ""), request.args.get("end", ""))
    query = (db.session.query(MenuItem.name, func.sum(OrderItem.quantity).label("quantity"), func.sum(OrderItem.quantity * (OrderItem.unit_price + OrderItem.option_total)).label("sales"))
             .join(OrderItem).join(Order).filter(Order.status == "paid", Order.created_at >= start_dt, Order.created_at <= end_dt)
             .group_by(MenuItem.id, MenuItem.name).order_by(func.sum(OrderItem.quantity).desc()))
    return render_template("reports/best_sellers.html", rows=query.all(), start=start, end=end)
