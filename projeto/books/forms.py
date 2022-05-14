from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Required

GENRES = [
    ('Secret Societies', 'Secret Societies'),
    ('Science Fiction', 'Science Fiction'),
    ('Spirituality', 'Spirituality',),
    ('Folk Tales', 'Folk Tales'),
    ('Psychology', 'Psychology'),
    ('Philosophy', 'Philosophy'),
    ('Dystopian', 'Dystopian'),
    ('Fantasy', 'Fantasy'),
    ('Horror', 'Horror'),
    ('Anime', 'Anime')
]

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    genre = SelectField('Genre', choices=GENRES, validators=[Required()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    image_book = FileField('Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')

CHOICES = [
    ('Extraordinary', 'Extraordinary'),
    ('Excelent', 'Excelent'),
    ('Great', 'Great',),
    ('Good', 'Good')
]

class AnalysisForm(FlaskForm):
    rating = SelectField('Rating', choices=CHOICES, validators=[Required()])
    review = TextAreaField('Review', validators=[DataRequired()])
    submit = SubmitField('Submit')