from datetime import datetime
from decimal import Decimal
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="staff")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.relationship("Order", backref="staff", lazy=True)
    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Table(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.String(10), unique=True, nullable=False)
    status = db.Column(db.String(20), default="available", nullable=False)
    orders = db.relationship("Order", backref="table", lazy=True)

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False, default="ทั่วไป")
    image_url = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    options = db.relationship("MenuOption", backref="menu_item", lazy=True, cascade="all, delete-orphan")
    order_items = db.relationship("OrderItem", backref="menu_item", lazy=True)

class MenuOption(db.Model):
    __tablename__ = "menu_options"
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer, db.ForeignKey("tables.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.String(20), default="open", nullable=False)
    order_type = db.Column(db.String(20), default="dine_in", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    items = db.relationship("OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")
    payment = db.relationship("Payment", backref="order", uselist=False, cascade="all, delete-orphan")
    @property
    def display_location(self): return f"โต๊ะ {self.table.table_number}" if self.table else "ซื้อกลับบ้าน"
    def recalculate_total(self):
        billable_items = [item for item in self.items if item.status not in {"cancelled", "sold_out"}]
        self.total_amount = sum((item.line_total for item in billable_items), Decimal("0.00"))

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey("menu_items.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    option_text = db.Column(db.String(255))
    option_total = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    status = db.Column(db.String(20), default="pending", nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    @property
    def line_total(self): return (self.unit_price + (self.option_total or Decimal("0.00"))) * self.quantity

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), unique=True, nullable=False)
    method = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    received_amount = db.Column(db.Numeric(10, 2))
    change_amount = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    paid_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
