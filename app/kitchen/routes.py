from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from app import db
from app.auth.permissions import roles_required
from app.models import Order, OrderItem

kitchen_bp = Blueprint("kitchen", __name__, url_prefix="/kitchen")
STATUSES = {"pending", "cooking", "ready", "served", "paused", "cancelled", "sold_out"}
STATUS_LABELS = {"pending": "รอทำ", "cooking": "กำลังทำ", "ready": "พร้อมเสิร์ฟ", "served": "เสิร์ฟแล้ว", "paused": "พักรายการ", "cancelled": "ยกเลิก", "sold_out": "อาหารหมด"}
KITCHEN_ORDER_STATUSES = ("open", "paid")
@kitchen_bp.route("/")
@login_required
@roles_required("admin", "kitchen", "staff")
def display():
    queue = (OrderItem.query.join(Order)
             .filter(Order.status.in_(KITCHEN_ORDER_STATUSES), OrderItem.status.notin_(["draft", "served", "cancelled"]))
             .order_by(OrderItem.created_at.asc()).all())
    grouped = {}
    for item in queue:
        grouped.setdefault(item.order, []).append(item)
    return render_template("kitchen/display.html", groups=list(grouped.items()), status_labels=STATUS_LABELS)

@kitchen_bp.route("/api/queue")
@login_required
@roles_required("admin", "kitchen", "staff")
def queue_api():
    count = (OrderItem.query.join(Order).filter(Order.status.in_(KITCHEN_ORDER_STATUSES), OrderItem.status.notin_(["draft", "served", "cancelled"])).count())
    return jsonify({"count": count})

@kitchen_bp.route("/item/<int:item_id>/status", methods=["POST"])
@login_required
@roles_required("admin", "kitchen", "staff")
def update_status(item_id):
    item = OrderItem.query.get_or_404(item_id)
    status = request.form.get("status")
    if status == "cancelled":
        flash("กรุณาใช้ปุ่มยกเลิกคิวเพื่อให้ระบบตรวจสอบยอดบิล", "warning")
    elif status in STATUSES:
        item.status = status
        db.session.commit()
    return redirect(url_for("kitchen.display"))

@kitchen_bp.route("/item/<int:item_id>/cancel", methods=["POST"])
@login_required
@roles_required("admin", "kitchen", "staff")
def cancel_queue_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    if item.order.payment or item.order.status == "paid":
        flash("ออเดอร์นี้ชำระเงินแล้ว หากต้องการยกเลิกต้องดำเนินการคืนเงินก่อน", "warning")
    elif item.status in {"served", "cancelled"}:
        flash("รายการนี้เสิร์ฟหรือยกเลิกไปแล้ว", "warning")
    else:
        item.status = "cancelled"
        item.order.recalculate_total()
        db.session.commit()
        flash("ยกเลิกรายการออกจากคิวแล้ว และปรับยอดบิลเรียบร้อย", "success")
    return redirect(url_for("kitchen.display"))
