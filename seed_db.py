from app import create_app, db
from app.models import MenuItem, MenuOption, Table, User
app = create_app()
with app.app_context():
    db.create_all()
    for username, password, role in [("admin", "admin1234", "admin"), ("staff1", "staff1234", "staff"), ("kitchen1", "kitchen1234", "kitchen")]:
        if not User.query.filter_by(username=username).first():
            user = User(username=username, role=role); user.set_password(password); db.session.add(user)
    if Table.query.count() == 0:
        for number in ["1", "2", "3", "4", "5", "6"]: db.session.add(Table(table_number=number))
    if MenuItem.query.count() == 0:
        samples = [("ผัดไทย", 60, "อาหารจานเดียว", ["เพิ่มไข่ดาว"]), ("ข้าวผัดกุ้ง", 70, "อาหารจานเดียว", ["พิเศษ"]), ("ต้มยำกุ้ง", 120, "ต้ม/แกง", ["เผ็ดน้อย", "เผ็ดปกติ", "เผ็ดมาก"]), ("ส้มตำ", 50, "ยำ/สลัด", ["ไม่เผ็ด", "เผ็ดน้อย", "เผ็ดปกติ"]), ("ชาเย็น", 30, "เครื่องดื่ม", ["หวานน้อย", "หวานปกติ"])]
        for name, price, category, options in samples:
            item = MenuItem(name=name, price=price, category=category)
            item.options = [MenuOption(name=option) for option in options]
            db.session.add(item)
    db.session.commit()
    print("สร้างฐานข้อมูลและข้อมูลตัวอย่างเรียบร้อยแล้ว")
