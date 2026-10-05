import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{Path(__file__).resolve().parent / 'instance' / 'pos_dev.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
