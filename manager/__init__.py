from flask import Flask
from flask_mail import Mail
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from apscheduler.schedulers.background import BackgroundScheduler

from manager.config import Config

db = SQLAlchemy()
admin = Admin(name='campaign_manager', template_mode='bootstrap3')
mail = Mail()
app = Flask(__name__)


def create_app(configuration=Config):
    app.config.from_object(configuration)
    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)

    from manager.model import Subscribers
    admin.add_view(ModelView(Subscribers, db.session))

    from manager.subscribers.routes import subs_bp
    from manager.subscribers.routes import send_email
    app.register_blueprint(subs_bp)

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(send_email, trigger='interval', hours=24)
    scheduler.start()

    try:
        return app
    except:
        scheduler.shutdown()
