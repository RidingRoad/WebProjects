# 最基本的启动工作
import datetime
import random

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from info import create_app
from info import models, db

# 选择配置模式,development/production
from info.models import User

app = create_app("development")
# 命令行方式(manager接管项目)启动项目
manager = Manager(app)
# 把falsk对象创建的数据表进行创表和迁移绑定

Migrate(app, db)
# 给数据库创表和迁移提供命令标识符mysql
manager.add_command("mysql", MigrateCommand)


@manager.option("-n", "--name", dest='name')
@manager.option("-p", "--password", dest="password")
def create_super_user(name, password):
    user = User()
    user.nick_name = name
    user.mobile = name
    user.is_admin = True
    user.password = password
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    print(app.url_map)
    manager.run()
