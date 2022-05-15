# Flask Library

![img](https://raw.githubusercontent.com/the-akira/Flask-Library/master/projeto/static/img/Avatar.png)

A simple library prototype using Python-Flask.

## Features

- Create Books
- Query Books
- Delete Books
- Update Books
- Analyze Books
- Search Mechanism
- User Registration & Login
- Account Info & Update

## Installation

### Clone the Repository

```
git clone https://github.com/the-akira/Flask-Library.git
```

### Inside the Main Directory

Create a Virtual Environment

```
python -m venv myvenv
```

Activate the Virtual Environment

```
source myvenv/bin/activate
```

Install Requirements

```
pip install -r requirements.txt
```

Run the Application

```
python run.py
```

Open your Web Browser and navigate to `http://127.0.0.1:5000/`.

## Managing the Database

### Inside the Main Directory

Start a new [Python REPL](https://python.land/introduction-to-python/the-repl) in your terminal:

```
python
```

Creating a new database:

```python
>>> from projeto import db
>>> db.create_all()
```

Initiating a new app context:

```python
>>> from projeto import create_app
>>> app = create_app()
>>> app.app_context().push()
```

Importing the database models:

```python
>>> from projeto.models import User, Book, Analysis
```

Inserting a new user in the database:

```python
>>> user = User(username='talantyr', email='talantyr@gmail.com', image_file='default.jpg', password='22447755')
>>> db.session.add(user)
>>> db.session.commit()
```

Querying for users in the database:

```python
>>> users = User.query.all()
>>> [user.email for user in users]
```

Search for a user with a specific ID:

```python
>>> User.query.get(1)
```

Order users by email in ascending order:

```python
>>> users = User.query.order_by(User.email.asc())
>>> [user for user in users]
```

Search for a specific user in the database:

```python
>>> users = User.query.filter(User.username.contains('aki'))
>>> [user for user in users]
```

Add a new book to the database with the current user:

```python
>>> book = Book(title='Quincas Borba', author='Machado de Assis', genre='História', summary='Clássico Brasileiro',user=user)
>>> db.session.add(book)
>>> db.session.commit()
```

Create a review for the book:

```python
>>> review = Analysis(rating='Muito bom!', review='Um livro altamente incrível', book_id=book.id, user=user)
>>> db.session.add(review)
>>> db.session.commit()
```

Have a good read!