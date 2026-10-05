from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.auth.permissions import roles_required
from app.models import Order, OrderItem

kitchen_bp = Blueprint("kitchen", __name__, url_prefix="/kitchen")
STATUSES = {"pending", "cooking", "ready", "served", "paused", "cancelled", "sold_out"}

@kitchen_bp.route("/")
@login_required
@roles_required("admin", "kitchen", "staff")
def display():
    queue = OrderItem.query.join(Order).filter(Order.status == "open", OrderItem.status.notin_(["served", "cancelled"])).order_by(OrderItem.created_at).all()
    return render_template("kitchen/display.html", queue=queue)

@kitchen_bp.route("/item/<int:item_id>/status", methods=["POST"])
@login_required
@roles_required("admin", "kitchen", "staff")
def update_status(item_id):
    item = OrderItem.query.get_or_404(item_id)
    status = request.form.get("status")
    if status in STATUSES: item.status = status; db.session.commit()
    return redirect(url_for("kitchen.display"))
