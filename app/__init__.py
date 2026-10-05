from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "กรุณาเข้าสู่ระบบก่อนใช้งาน"
    from app.auth.routes import auth_bp
    from app.menu.routes import menu_bp
    from app.order.routes import order_bp
    from app.kitchen.routes import kitchen_bp
    from app.billing.routes import billing_bp
    from app.reports.routes import reports_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(menu_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(kitchen_bp)
    app.register_blueprint(billing_bp)
    app.register_blueprint(reports_bp)
    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))
