from projeto import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin

# >>> from projeto import create_app
# >>> app = create_app()
# >>> app.app_context().push()
# >>> from projeto.models import User
# >>> from projeto import db
# >>> db.create_all()
# >>> user_1 = User(username='akira', email='akira@gmail.com', password='akira123')
# >>> db.session.add(user_1)
# >>> db.session.commit()
# >>> User.query.all()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	Book = db.relationship('Book', backref='user', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	author = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	summary = db.Column(db.Text, nullable=False)	
	image_book = db.Column(db.String(20), nullable=False, default='book_default.jpg')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Book('{self.title}', '{self.date_posted}')"