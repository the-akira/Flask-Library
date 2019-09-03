from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from projeto import db, bcrypt
from projeto.models import User, Book
from projeto.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"]) # Permite os métodos GET e POST para essa rota
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created! You are now able to log in', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form) # Passamos a instância da form para o nosso template

@users.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	return render_template('login.html', form=form)