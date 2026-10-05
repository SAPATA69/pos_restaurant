from datetime import datetime, time
from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func
from app import db
from app.auth.permissions import roles_required
from app.models import MenuItem, Order, OrderItem
reports_bp = Blueprint("reports", __name__, url_prefix="/reports")
@reports_bp.route("/best-sellers")
@login_required
@roles_required("admin", "staff")
def best_sellers():
    start, end = request.args.get("start", ""), request.args.get("end", "")
    query = db.session.query(MenuItem.name, func.sum(OrderItem.quantity).label("quantity"), func.sum(OrderItem.quantity * OrderItem.unit_price).label("sales")).join(OrderItem).join(Order).filter(Order.status == "paid").group_by(MenuItem.id, MenuItem.name).order_by(func.sum(OrderItem.quantity).desc())
    if start: query = query.filter(Order.created_at >= datetime.combine(datetime.strptime(start, "%Y-%m-%d").date(), time.min))
    if end: query = query.filter(Order.created_at <= datetime.combine(datetime.strptime(end, "%Y-%m-%d").date(), time.max))
    return render_template("reports/best_sellers.html", rows=query.all(), start=start, end=end)
