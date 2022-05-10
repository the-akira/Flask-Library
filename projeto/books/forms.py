from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[DataRequired()])
    image_book = FileField('Book Picture', validators=[DataRequired(),FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')