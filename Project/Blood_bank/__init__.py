from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Blood_bank.config import Config

app = Flask(__name__)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)


from Blood_bank.main.routes import main
from Blood_bank.app_admin.routes import app_admin
from Blood_bank.bloodbank_admin.routes import bloodbank_admin
from Blood_bank.app_users.routes import users
from Blood_bank.bloodbanks.routes import bloodbanks
from Blood_bank.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(app_admin)
app.register_blueprint(bloodbank_admin)
app.register_blueprint(users)
app.register_blueprint(bloodbanks)
app.register_blueprint(errors)