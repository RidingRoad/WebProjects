from flask import  Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

app.config.from_object(Config)


db = SQLAlchemy(app)

# user table
# users: John/Tom
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return 'User name=%s'%self.name



# Roles table
# role: admin/common
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    us = db.relationship('User',backref='roles')
    def __repr__(self):
        return 'Role name=%s'%self.name


@app.route('/')
def index():
    return "index page"


if __name__ == "__main__":
    # drop tabel
    db.drop_all()
    # # create table
    db.create_all()
    # # create column data
    # user = User()
    # # specific data
    # user.name = "RidingRoad"
    # user.password = "RidingRoad"
    # user.email = "RidingRoad@163.com"
    # # add data and commit data by db.session.add(object)/commit()
    # db.session.add(user)
    # db.session.commit()
    ro1 = Role(name='admin')
    db.session.add(ro1)
    db.session.commit()
    # 再次插入一条数据
    ro2 = Role(name='user')
    db.session.add(ro2)
    db.session.commit()

    us1 = User(name='wang', email='wang@163.com', password='123456', role_id=ro1.id)
    us2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=ro2.id)
    us3 = User(name='chen', email='chen@126.com', password='987654', role_id=ro2.id)
    us4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=ro1.id)
    us5 = User(name='tang', email='tang@itheima.com', password='158104', role_id=ro2.id)
    us6 = User(name='wu', email='wu@gmail.com', password='5623514', role_id=ro2.id)
    us7 = User(name='qian', email='qian@gmail.com', password='1543567', role_id=ro1.id)
    us8 = User(name='liu', email='liu@itheima.com', password='867322', role_id=ro1.id)
    us9 = User(name='li', email='li@163.com', password='4526342', role_id=ro2.id)
    us10 = User(name='sun', email='sun@163.com', password='235523', role_id=ro2.id)
    db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    db.session.commit()

    app.run()