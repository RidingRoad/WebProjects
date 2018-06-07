from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)

class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = True


app.config.from_object(Config)
#
db = SQLAlchemy(app)

manager = Manager(app)
# 创建迁移框架
# 第一个参数表示app对象
# 第二个参数表示数据库对象
Migrate(app,db)
# 第一个参数随意写,在使用迁移命令的时候使用
# 第二个参数接受MigrateCommand
manager.add_command("xxx",MigrateCommand)


# 角色表
# db.Model:固定的写法
# 管理员，普通用户
# 管理员：张三
# 普通用户：李四和王五
# 一的一方
class Role(db.Model):
    # 定义表名：固定的写法，__tablename__
    # roles:表的名字随意取
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    title = db.Column(db.String(128))
    # relationship:固定写法，在一对多的时候，在一的一方定义关系
    # backref:固定写法，表示的是反推
    # 第一个参数：表示要关联的类的模型
    # 第二个参数：表示新增加的一个属性，属性的名字随意取
    us = db.relationship("User",backref = "role")
    # 当前函数的作用是返回友好的用户体验
    def __repr__(self):
        return "Role = %s"%self.name

# 用户表
# 张三，李四，王五
# 多的一方
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(128))
    email  = db.Column(db.String(128))
    # ForeignKey:在多的一方定义外键
    role_id = db.Column(db.Integer,db.ForeignKey("roles.id"))

    def __repr__(self):
        return "User = %s"%self.name


@app.route("/")
def index():
    return "index page"

if __name__ == '__main__':
    # 删除表
    db.drop_all()
    # 创建表
    # db.create_all()
    #
    # ro1 = Role(name='admin')
    # db.session.add(ro1)
    # db.session.commit()
    # # 再次插入一条数据
    # ro2 = Role(name='user')
    # db.session.add(ro2)
    # db.session.commit()
    #
    # us1 = User(name='wang', email='wang@163.com', password='123456', role_id=ro1.id)
    # us2 = User(name='zhang', email='zhang@189.com', password='201512', role_id=ro2.id)
    # us3 = User(name='chen', email='chen@126.com', password='987654', role_id=ro2.id)
    # us4 = User(name='zhou', email='zhou@163.com', password='456789', role_id=ro1.id)
    # us5 = User(name='tang', email='tang@itheima.com', password='158104', role_id=ro2.id)
    # us6 = User(name='wu', email='wu@gmail.com', password='5623514', role_id=ro2.id)
    # us7 = User(name='qian', email='qian@gmail.com', password='1543567', role_id=ro1.id)
    # us8 = User(name='liu', email='liu@itheima.com', password='867322', role_id=ro1.id)
    # us9 = User(name='li', email='li@163.com', password='4526342', role_id=ro2.id)
    # us10 = User(name='sun', email='sun@163.com', password='235523', role_id=ro2.id)
    # db.session.add_all([us1, us2, us3, us4, us5, us6, us7, us8, us9, us10])
    # db.session.commit()

    # user = User()
    # user.name = "itcast"
    # user.password = "123"
    # user.email = "123@itcast.cn"
    # # 往数据库里面添加一条数据
    # db.session.add(user)
    # db.session.commit()


    manager.run()