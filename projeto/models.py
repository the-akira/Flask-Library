from projeto import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    analysis = db.relationship('Analysis', backref='user', lazy=True)
    Book = db.relationship('Book', backref='user', lazy=True)
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    summary = db.Column(db.Text, nullable=False)	
    image_book = db.Column(db.String(20), nullable=True, default='book_default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    analysis = db.relationship('Analysis', backref='book', lazy=True)

    def __repr__(self):
        return f"Book('{self.title}', '{self.date_posted}')"

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f"Analysis('{self.user_id}', '{self.rating}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)