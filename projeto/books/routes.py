from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from projeto import db
from projeto.models import Book
from projeto.books.forms import BookForm
from projeto.books.utils import save_book_picture

books = Blueprint('books', __name__)

@books.route("/book/new", methods=["GET", "POST"])
@login_required
def new_book():
	form = BookForm()
	if form.validate_on_submit():
		print(form.image_book.data)
		if form.image_book.data:
			picture_file = save_book_picture(form.image_book.data)
			book = Book(title=form.title.data, author=form.author.data, summary=form.summary.data, image_book=picture_file, user=current_user)
			db.session.add(book)
			db.session.commit()
		flash('Your book has been added!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_book.html', title='New Book', form=form, legend='New Book')