# POS ร้านอาหาร + ระบบคิวครัว

เว็บแอปพลิเคชันต้นแบบด้วย Flask และ PostgreSQL รองรับนั่งรับประทานที่ร้าน/ซื้อกลับบ้าน, คิวครัว, ตัวเลือกอาหาร, ใบเสร็จ และ QR Payment แบบทดลอง

## Workflow หลัก

1. พนักงานเพิ่มอาหารลงบิลในสถานะ **ยังไม่ส่งครัว (Draft)**
2. กด **ส่งรายการใหม่เข้าคิวครัว**
3. ครัวกด **เริ่มทำ → พร้อมเสิร์ฟ → เสิร์ฟแล้ว**
4. แคชเชียร์รับชำระเงินและพิมพ์ใบเสร็จ

## QR Payment

โหมด `QR ทดลอง` สร้าง QR Code ในหน้า checkout ด้วย QR payload สำหรับการสาธิตเท่านั้น ไม่ได้เชื่อมต่อธนาคารจริง หากต้องการใช้จริงให้ตั้งค่า `PROMPTPAY_ID` เป็นหมายเลขบัญชี/พร้อมเพย์ของร้าน และพัฒนาตัวสร้าง Thai QR Payment ตามมาตรฐานธนาคารก่อนใช้งานจริง

## ตั้งค่าและรัน

```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python seed_db.py
python run.py
```

เปิด `http://localhost:5000` หรือ `http://localhost:5000/auth/login`

## บัญชีทดสอบ

| บทบาท | Username | Password |
|---|---|---|
| ผู้ดูแลระบบ | admin | admin1234 |
| พนักงาน/แคชเชียร์ | staff1 | staff1234 |
| ครัว | kitchen1 | kitchen1234 |

## การตั้งค่าเสริมผ่าน `.env`

```env
SECRET_KEY=change-me
DATABASE_URL=postgresql://postgres:password@localhost:5432/pos_restaurant
RESTAURANT_NAME=ครัวอุบล POS
RESTAURANT_PHONE=โทร. 08X-XXX-XXXX
PROMPTPAY_ID=0812345678
```
