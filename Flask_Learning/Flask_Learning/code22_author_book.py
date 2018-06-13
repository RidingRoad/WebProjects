from  flask import Flask,render_template,redirect,url_for,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/author_book'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = 'adsfsafsaasafas'

app.config.from_object(Config)


db = SQLAlchemy(app)

class AuthorBookForm(FlaskForm):
    author_name = StringField(label="author",validators=[DataRequired('input author name')])
    book_name = StringField(label="book", validators=[DataRequired('input book name')])
    submit = SubmitField('add')


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    books = db.relationship('Book',backref='author')


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))

@app.route("/delete_book/<book_id>")
def delete_book(book_id):
    book = Book.query.get(book_id)
    # delete book
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    return redirect(url_for('index'))

@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    author = Author.query.get(author_id)
    Book.query.filter(Book.author_id == author_id).delete()
    db.session.delete(author)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/',methods=['POST','GET'])
def index():
    form = AuthorBookForm()
    if form.validate_on_submit():
        # request.form.get('authon_name')
        #the above method is only in html page to get form data
        author_name = form.author_name.data
        # the above method is using in wtforms
        book_name = form.book_name.data
        # add the author to database
        author = Author()
        author.name = author_name
        db.session.add(author)
        db.session.commit()

        # add the book name to the database
        book = Book()
        book.name = book_name
        book.author_id = author.id
        db.session.add(book)
        db.session.commit()
    author_li = Author.query.all()
    return render_template("code22_author_book.html",form=form,authors=author_li)






#
# @app.route('/')
# def index():
#     form = AuthorBookForm()
#     author_li = Author.query.all()
#     return render_template('code22_author_book.html',form = form,authors=author_li)

if __name__ == "__main__":
    db.drop_all()
    db.create_all()
    # 生成数据
    au1 = Author(name='老王')
    au2 = Author(name='老尹')
    au3 = Author(name='老刘')
    # 把数据提交给用户会话
    db.session.add_all([au1, au2, au3])
    # 提交会话
    db.session.commit()
    bk1 = Book(name='老王回忆录', author_id=au1.id)
    bk2 = Book(name='我读书少，你别骗我', author_id=au1.id)
    bk3 = Book(name='如何才能让自己更骚', author_id=au2.id)
    bk4 = Book(name='怎样征服美丽少女', author_id=au3.id)
    bk5 = Book(name='如何征服英俊少男', author_id=au3.id)
    # 把数据提交给用户会话
    db.session.add_all([bk1, bk2, bk3, bk4, bk5])
    # 提交会话
    db.session.commit()
    app.run(debug=True)