from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("order.select_table"))
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username", "").strip()).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user)
            return redirect(url_for("kitchen.display" if user.role == "kitchen" else "order.select_table"))
        flash("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user(); return redirect(url_for("auth.login"))
