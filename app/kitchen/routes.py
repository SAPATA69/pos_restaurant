from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from app import db
from app.models import OrderItem

kitchen_bp = Blueprint("kitchen", __name__, url_prefix="/kitchen")


@kitchen_bp.route("/")
@login_required
def display():
    queue = OrderItem.query.filter(OrderItem.status != "served").order_by(OrderItem.created_at).all()
    return render_template("kitchen/display.html", queue=queue)


@kitchen_bp.route("/item/<int:item_id>/status", methods=["POST"])
@login_required
def update_status(item_id):
    item = OrderItem.query.get_or_404(item_id)
    item.status = request.form.get("status")
    db.session.commit()
    return redirect(url_for("kitchen.display"))
