import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{Path(__file__).resolve().parent / 'instance' / 'pos_dev.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTAURANT_NAME = os.environ.get("RESTAURANT_NAME", "ครัวอุบล POS")
    RESTAURANT_PHONE = os.environ.get("RESTAURANT_PHONE", "โทร. 08X-XXX-XXXX")
    PROMPTPAY_ID = os.environ.get("PROMPTPAY_ID", "0812345678")
