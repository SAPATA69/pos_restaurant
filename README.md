# POS ร้านอาหาร + ระบบคิวครัว

เว็บแอปพลิเคชันต้นแบบสำหรับโครงงานคณะวิทยาการคอมพิวเตอร์ พัฒนาด้วย Flask และ PostgreSQL รองรับการรับประทานที่ร้านและซื้อกลับบ้าน

## ฟังก์ชันหลัก

- Login แยกบทบาท `admin`, `staff`, `kitchen`
- จัดการโต๊ะ: ว่าง, กำลังใช้งาน, รอชำระเงิน
- จัดการเมนูและสถานะพร้อมขาย/อาหารหมด
- ตัวเลือกเพิ่มเติมและหมายเหตุของรายการอาหาร
- POS เพิ่มหลายรายการในออเดอร์เดียว
- คิวครัวเรียงตามเวลาและแยกตามโต๊ะ/ออเดอร์
- สถานะรายการ: รอทำ, กำลังทำ, ทำเสร็จ, เสิร์ฟแล้ว, พักรายการ, ยกเลิก, อาหารหมด
- ชำระเงิน: เงินสด, โอนเงิน, QR Payment แบบทดลอง
- ใบเสร็จและหน้าสำหรับพิมพ์
- รายงานเมนูขายดีพร้อมตัวกรองวันที่

## เทคโนโลยี

Flask, Flask-SQLAlchemy, Flask-Migrate, PostgreSQL, SQLAlchemy ORM, Jinja2, HTML/CSS/JavaScript และ Bootstrap 5

## การติดตั้ง

```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

ตั้งค่า `.env` สำหรับ PostgreSQL:

```env
DATABASE_URL=postgresql://postgres:รหัสผ่าน@localhost:5432/pos_restaurant
SECRET_KEY=เปลี่ยนเป็นคีย์ลับของโครงการ
```

สร้างฐานข้อมูลและข้อมูลตัวอย่าง:

```bash
python seed_db.py
python run.py
```

หากใช้ Flask-Migrate กับฐานข้อมูลที่มีอยู่แล้ว:

```bash
flask --app run.py db init
flask --app run.py db migrate -m "initial POS schema"
flask --app run.py db upgrade
```

## บัญชีทดสอบ

| บทบาท | Username | Password |
|---|---|---|
| ผู้ดูแลระบบ | admin | admin1234 |
| พนักงาน/แคชเชียร์ | staff1 | staff1234 |
| ครัว | kitchen1 | kitchen1234 |

โค้ดชุดนี้เป็นต้นแบบสำหรับการนำเสนอและต่อยอด ยังไม่ได้เชื่อมต่อระบบจ่ายเงินหรือเครื่องพิมพ์จริง และยังไม่ได้ Push ขึ้น Git ตามคำขอ
