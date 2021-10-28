from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Thou shall not pass (without first logging in)!'
login_manager.login_message_category = 'danger'

mail = Mail(app)

from app.blueprints.auth import bp as auth
app.register_blueprint(auth)

from app.blueprints.blog import bp as blog
app.register_blueprint(blog)

from app.blueprints.api import bp as api
app.register_blueprint(api)

from app import routes


