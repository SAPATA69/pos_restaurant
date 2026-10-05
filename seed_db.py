"""
รันครั้งแรกเพื่อสร้างตารางในฐานข้อมูล และใส่ข้อมูลตัวอย่าง
คำสั่ง: python seed_db.py
"""
from app import create_app, db
from app.models import User, Table, MenuItem

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        admin.set_password("admin1234")
        db.session.add(admin)

    if not User.query.filter_by(username="staff1").first():
        staff = User(username="staff1", role="staff")
        staff.set_password("staff1234")
        db.session.add(staff)

    if not User.query.filter_by(username="kitchen1").first():
        kitchen = User(username="kitchen1", role="kitchen")
        kitchen.set_password("kitchen1234")
        db.session.add(kitchen)

    if Table.query.count() == 0:
        for n in ["1", "2", "3", "4", "5"]:
            db.session.add(Table(table_number=n))

    if MenuItem.query.count() == 0:
        sample_items = [
            ("ผัดไทย", 60, "อาหารจานเดียว"),
            ("ข้าวผัดกุ้ง", 70, "อาหารจานเดียว"),
            ("ต้มยำกุ้ง", 120, "ต้ม/แกง"),
            ("ส้มตำ", 50, "ยำ/สลัด"),
            ("ชาเย็น", 30, "เครื่องดื่ม"),
        ]
        for name, price, category in sample_items:
            db.session.add(MenuItem(name=name, price=price, category=category))

    db.session.commit()
    print("สร้างฐานข้อมูลและข้อมูลตัวอย่างเรียบร้อยแล้ว")
    print("บัญชีทดสอบ: admin/admin1234, staff1/staff1234, kitchen1/kitchen1234")
