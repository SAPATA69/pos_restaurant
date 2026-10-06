from decimal import Decimal, InvalidOperation
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
        order = Order(user_id=current_user.id, order_type="takeaway")
        db.session.add(order)
        db.session.commit()
    return redirect(url_for("order.take_order", order_id=order.id))

@order_bp.route("/table/<int:table_id>")
@login_required
@roles_required("admin", "staff")
def open_table(table_id):
    table = Table.query.get_or_404(table_id)
    order = Order.query.filter_by(table_id=table.id, status="open").first()
    if not order:
        order = Order(table_id=table.id, user_id=current_user.id, order_type="dine_in")
        table.status = "occupied"
        db.session.add(order)
        db.session.commit()
    return redirect(url_for("order.take_order", order_id=order.id))

@order_bp.route("/<int:order_id>", methods=["GET", "POST"])
@login_required
@roles_required("admin", "staff")
def take_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.status != "open":
        flash("ออเดอร์นี้ปิดไปแล้ว ไม่สามารถเพิ่มรายการได้", "warning")
        return redirect(url_for("billing.receipt", order_id=order.id))
    if request.method == "POST":
        menu_item = MenuItem.query.get_or_404(int(request.form["menu_item_id"]))
        if not menu_item.is_available:
            flash("เมนูนี้หมดชั่วคราว", "warning")
            return redirect(url_for("order.take_order", order_id=order.id))
        try:
            quantity = max(1, int(request.form.get("quantity", 1)))
        except (TypeError, ValueError):
            quantity = 1
        option_ids = request.form.getlist("option_ids")
        selected = [option for option in menu_item.options if str(option.id) in option_ids and option.is_available]
        item = OrderItem(
            order=order, menu_item=menu_item, quantity=quantity, unit_price=menu_item.price,
            option_text=", ".join(option.name for option in selected) or None,
            option_total=sum((option.price for option in selected), Decimal("0")),
            note=request.form.get("note", "").strip() or None,
            status="draft",
        )
        db.session.add(item)
        db.session.flush()
        order.recalculate_total()
        db.session.commit()
        flash("เพิ่มรายการในบิลแล้ว กดส่งเข้าครัวเมื่อพร้อม", "success")
        return redirect(url_for("order.take_order", order_id=order.id))
    return render_template("order/take_order.html", order=order, menu_items=MenuItem.query.filter_by(is_available=True).order_by(MenuItem.category, MenuItem.name).all())

@order_bp.route("/<int:order_id>/item/<int:item_id>/remove", methods=["POST"])
@login_required
@roles_required("admin", "staff")
def remove_draft_item(order_id, item_id):
    order = Order.query.get_or_404(order_id)
    item = OrderItem.query.filter_by(id=item_id, order_id=order.id).first_or_404()
    if order.status != "open" or item.status != "draft":
        flash("ลบได้เฉพาะรายการที่ยังไม่ส่งเข้าครัวเท่านั้น", "warning")
    else:
        db.session.delete(item)
        db.session.flush()
        order.recalculate_total()
        db.session.commit()
        flash("ลบรายการที่ยังไม่ส่งครัวแล้ว", "success")
    return redirect(url_for("order.take_order", order_id=order.id))

@order_bp.route("/<int:order_id>/send", methods=["POST"])
@login_required
@roles_required("admin", "staff")
def send_to_kitchen(order_id):
    order = Order.query.get_or_404(order_id)
    draft_items = [item for item in order.items if item.status == "draft"]
    if not draft_items:
        flash("ไม่มีรายการใหม่ที่ต้องส่งเข้าครัว", "warning")
    else:
        for item in draft_items:
            item.status = "pending"
        db.session.commit()
        flash(f"ส่ง {len(draft_items)} รายการเข้าคิวครัวแล้ว", "success")
    return redirect(url_for("order.take_order", order_id=order.id))
