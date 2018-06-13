# _*_ coding:utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# set the config about the sqlalchemy
class Config():
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/sqlalchemy_test"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app.config.from_object(Config)

db = SQLAlchemy(app)


class Role(db.Model):
    # define the tablename
    __tablename__ = "roles"
    # define the column object
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    us = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "Role:%s" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=True)
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))

    def __repr__(self):
        return "Role:%s" % self.name


@app.route('/')
def index():
    return "start the sqlchemy"


if __name__ == "__main__":
    app.run(debug=True)
