from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.secret_key = "djjajfdasjjd"

# to set the database
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:mysql@127.0.0.1:3306/author_book"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class AddBookForm(FlaskForm):
    # set the book form to add to the database
    author = StringField(label='author:', validators=[InputRequired("input the author name")])
    book = StringField(label='book name:', validators=[InputRequired("input the book name")])
    submit = SubmitField(label='add')


class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    # 定义属性，以便作者模型可以直接通过该属性访问其多的一方的数据(书的数据)
    # backref 给 Book 也添加了一个 author 的属性，可以通过 book.author 获取 book 所对应的作者信息
    author_books = db.relationship("Book", backref="author")


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey(Author.id))


@app.route('/delete_author/<author_id>')
def delete_author(author_id):
    try:
        author = Author.query.get(author_id)
    except Exception as e:
        print(e)
        return "query error"
    if not author:
        return "author not exists"
    try:
        Book.query.filter(Book.author_id == author_id).delete()

        db.session.delete(author)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return "failed to delete author"
    return redirect(url_for('index'))


@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
    except Exception as e:
        print(e)
        return "query error"
    if not book:
        return "book doesn't exist"
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return "failed to delete book"
    return redirect(url_for('index'))


@app.route("/", methods=["get", "post"])
def index():
    book_form = AddBookForm()
    if book_form.validate_on_submit():
        author_name = book_form.author.data
        book_name = book_form.book.data
        author = Author.query.filter(Author.name == author_name).first()
        # print(author)
        if not author:
            try:
                author = Author(name=author_name)
                db.session.add(author)
                db.session.commit()

                book = Book(name=book_name, author_id=author.id)
                db.session.add(book)
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                print(e)
                flash("New author failed to add book")
        else:
            # to judge the book exists or not
            book = Book.query.filter(Book.name == book_name).first()

            if not book:
                try:
                    # add the book to the database
                    book = Book(name=book_name, author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    flash("Exists author failed to add book")
            else:
                flash("already exists")
    else:
        if request.method == "POST":
            flash("parameters error")

    # query data

    authors = Author.query.all()
    return render_template("demo2_author_book.html", authors=authors, form=book_form)


if __name__ == "__main__":
    db.drop_all()
    db.create_all()
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
