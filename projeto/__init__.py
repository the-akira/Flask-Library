from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from projeto.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)

	bcrypt.init_app(app)
	login_manager.init_app(app)

	from projeto.users.routes import users
	from projeto.main.routes import main
	app.register_blueprint(main)
	app.register_blueprint(users)

	return app