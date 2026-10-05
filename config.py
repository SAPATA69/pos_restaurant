import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-this")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:password@localhost:5432/pos_restaurant"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
