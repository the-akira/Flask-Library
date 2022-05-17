from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from projeto import db, bcrypt
from projeto.models import User, Book, Message
from projeto.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, MessageForm
from projeto.utils.utils import save_picture
from collections import Counter
from datetime import datetime

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
    return render_template('register.html', title='Register', form=form) # Passamos a instância do form para o nosso template

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form) # Passamos a instância do form para o nosso template

@users.route("/logout")
def logout():
    flash(f'{current_user.username} logged out.', 'success')
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'static/profile', 350, 350)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile/' + current_user.image_file)
    books = sorted([(book.id, book.author, book.title, book.genre, book.date_posted, len(book.analysis)) for book in current_user.Book], key=lambda book: book[2])
    total_analysis = len(current_user.analysis)
    total_books = len(books)
    books_author = dict(Counter(sorted([book.author for book in current_user.Book])))
    books_genre = dict(Counter([book.genre for book in current_user.Book]).most_common())
    return render_template(
        'account.html', 
        title='Account', 
        image_file=image_file, 
        form=form, 
        books=books,
        total_books=total_books, 
        total_analysis=total_analysis,
        books_author=books_author, 
        books_genre=books_genre
    )

@users.route("/user/<string:username>")
def user_book(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.filter_by(user=user).order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_books.html', books=books, user=user)

@users.route('/send_message/<string:recipient>/<string:page>', methods=['GET', 'POST'])
@login_required
def send_message(recipient, page):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(author=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash(f'Your message has been sent to {user.username}', 'success')
        if page == 'messages':
            return redirect(url_for('users.messages'))  
        elif page == 'user':
            return redirect(url_for('users.user_book', username=recipient))
    return render_template('message.html', form=form, recipient=recipient, page=page)

@users.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages = current_user.messages_received.order_by(
        Message.timestamp.desc()).paginate(page, 5, False)
    next_url = url_for('users.messages', page=messages.next_num) \
        if messages.has_next else None
    prev_url = url_for('users.messages', page=messages.prev_num) \
        if messages.has_prev else None
    return render_template('messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, total_messages=messages.total)

@users.route("/message/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.author == current_user:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted', 'success')
    return redirect(url_for('users.messages'))

@users.route("/message/delete_all", methods=["POST"])
@login_required
def delete_all_messages():
    messages = Message.query.filter_by(recipient_id=current_user.id).all()
    for message in messages:
        if message.author == current_user:
            abort(403)      
        db.session.delete(message)
    db.session.commit()
    flash('All Messages deleted', 'success')
    return redirect(url_for('users.messages'))