from flask import Flask, render_template
from flask import flash
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired
from flask_sqlalchemy import  SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "DJKLLKDFJASJEWIIUDFJSAJF"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/author_book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

class Append(FlaskForm):
    au_info = StringField(label="author",validators=[DataRequired("must input the authors' name")])
    bk_info = StringField(label="book_name",validators=[DataRequired("must input the book name")])
    submit = SubmitField("add")

class Author(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),unique=True)
    au_book = db.relationship("Book",backref = "author")

    def __repr__(self):
        return "Author:%s" %self.name

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(38))
    author_id = db.Column(db.Integer,db.ForeignKey("authors.id"))
    def __repr__(self):
        return "Book:%s"%self.name



@app.route("/",methods=["GET","POST"])
def index():

    append_form = Append()
    if request.method == "POST":
        if append_form.validate_on_submit():
            author_name  = append_form.au_info.data
            book_name = append_form.bk_info.data
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                try:
                    # to add the author
                    author = Author(name=author_name)
                    db.session.add(author)
                    db.session.commit()
                    # to add the book into database
                    book = Book(name = book_name,author_id=author.id)
                    db.session.add(book)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    flash("some wrong to add the book")
            else:
                book_names = [book.name for book in Book.query.all()]
                if book_name in book_names:
                    flash("already have the book")
                else:
                    try:
                        book = Book(name=book_name, author_id=author.id)
                        db.session.add(book)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
                        flash('数据添加错误')
                    else:
                        flash('数据输入有问题')
    authors = Author.query.all()
    books = Book.query.all()
    return render_template("code22_my_author_book.html",append_form = append_form,authors=authors,books=books)

if __name__ == "__main__":

    app.run(debug=True)