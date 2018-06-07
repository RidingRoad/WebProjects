from  flask import Flask,render_template

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)


class AuthorBookForm(FlaskForm):
    author_name = StringField(label="author",validators=[DataRequired('input author name')])
    book_name = StringField(label="book", validators=[DataRequired('input book name')])
    submit = SubmitField('add')

@app.route('/')
def index():
    return render_template('code22_author_book.html')

if __name__ == "__main__":
    app.run()