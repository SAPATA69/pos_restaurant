# POS ร้านอาหาร + ระบบคิวครัว (Kitchen Order Ticket System)

## โครงสร้างโปรเจกต์
```
pos_restaurant/
├── app/
│   ├── __init__.py        # App factory
│   ├── models.py          # SQLAlchemy models
│   ├── auth/               # login/logout
│   ├── menu/                # จัดการเมนู (CRUD)
│   ├── order/                # เลือกโต๊ะ + รับออเดอร์
│   ├── kitchen/              # หน้าจอครัว (คิวออเดอร์)
│   ├── billing/               # คิดเงิน/ปิดบิล
│   ├── static/
│   └── templates/
├── config.py
├── run.py
├── seed_db.py              # สร้างตาราง + ข้อมูลตัวอย่าง
└── requirements.txt
```

## ขั้นตอนติดตั้ง (รันทีละคำสั่ง)

### 1. ติดตั้ง PostgreSQL (ถ้ายังไม่มี)
Windows: โหลดจาก https://www.postgresql.org/download/windows/
Mac: `brew install postgresql`
Linux: `sudo apt install postgresql`

### 2. สร้างฐานข้อมูล
```bash
psql -U postgres
CREATE DATABASE pos_restaurant;
\q
```

### 3. สร้าง virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 4. ติดตั้งแพ็กเกจทั้งหมด
```bash
pip install -r requirements.txt
```

### 5. ตั้งค่าการเชื่อมต่อฐานข้อมูล
แก้ไขใน `config.py` หรือสร้างไฟล์ `.env`:
```
DATABASE_URL=postgresql://postgres:รหัสผ่านของคุณ@localhost:5432/pos_restaurant
SECRET_KEY=your-secret-key
```

### 6. สร้างตารางในฐานข้อมูล + ข้อมูลตัวอย่าง
```bash
python seed_db.py
```

### 7. รันเซิร์ฟเวอร์
```bash
python run.py
```
เปิดเบราว์เซอร์ที่ http://127.0.0.1:5000/auth/login

### บัญชีทดสอบ
| บทบาท | Username | Password |
|---|---|---|
| ผู้ดูแลระบบ | admin | admin1234 |
| พนักงานเสิร์ฟ | staff1 | staff1234 |
| ครัว | kitchen1 | kitchen1234 |

## ฟีเจอร์ที่มีในโครงร่างนี้
- [x] ระบบ Login แยก role (admin/staff/kitchen)
- [x] จัดการเมนูอาหาร (เพิ่มเมนู)
- [x] เลือกโต๊ะ + เปิดออเดอร์ + เพิ่มรายการอาหาร
- [x] หน้าจอครัว (Kitchen Display) แสดงคิว + อัปเดตสถานะ
- [x] คิดเงิน + ปิดบิล + คืนสถานะโต๊ะเป็นว่าง

## สิ่งที่ยังต้องทำต่อ (ตามแผน)
- ปรับ UI ให้สวยขึ้น (ตอนนี้เป็น HTML พื้นฐานล้วนๆ)
- เพิ่มหน้ารายงานยอดขายรายวัน
- แก้ไข/ลบเมนู (ตอนนี้มีแค่เพิ่ม)
- ทดสอบ flow ทั้งหมดแล้วจดบันทึกผล/ปัญหาไว้ใช้เขียนบทที่ 4
