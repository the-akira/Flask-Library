from flask import render_template, request, Blueprint
from projeto.models import Book

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
	page = request.args.get('page', 1, type=int)
	books = Book.query.order_by(Book.date_posted.desc()).paginate(page=page, per_page=5)
	return render_template('home.html', books=books)