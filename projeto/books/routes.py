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

@books.route("/book/<int:book_id>")
def book(book_id):
	book = Book.query.get_or_404(book_id)
	return render_template('book.html', book=book)

@books.route("/book/<int:book_id>/delete", methods=["POST"])
@login_required
def delete_book(book_id):
	book = Book.query.get_or_404(book_id)
	if book.user != current_user:
		abort(403)
	db.session.delete(book)
	db.session.commit()
	flash('Your book has been deleted', 'success')
	return redirect(url_for('main.home'))

@books.route("/book/<int:book_id>/update", methods=["GET", "POST"])
@login_required
def update_book(book_id):
	book = Book.query.get_or_404(book_id)
	if book.user != current_user:
		abort(403)
	form = BookForm()
	if form.validate_on_submit():
		if form.image_book.data:
			picture_file = save_book_picture(form.image_book.data)
			book.title = form.title.data
			book.author = form.author.data
			book.summary = form.summary.data 
			book.image_book = picture_file
			db.session.commit()
			flash('Your book has been updated', 'success')
			return redirect(url_for('books.book', book_id=book.id))
	elif request.method == 'GET':
		# Preenche os formulários com os dados atuais do post
		form.title.data = book.title
		form.author.data = book.author
		form.summary.data = book.summary
		form.image_book.data = book.image_book
	return render_template('create_book.html', form=form, legend='Update Book')