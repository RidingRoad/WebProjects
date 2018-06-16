# 最基本的启动工作
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


from info import create_app
from info import models, db

# 选择配置模式,development/production
app = create_app("development")
# 命令行方式(manager接管项目)启动项目
manager = Manager(app)
# 把falsk对象创建的数据表进行创表和迁移绑定

Migrate(app, db)
# 给数据库创表和迁移提供命令标识符mysql
manager.add_command("mysql", MigrateCommand)

@app.route("/<int:news_id>")
def news_detail(news_id):
    print(news_id)
    return news_id



if __name__ == "__main__":
    print(app.url_map)
    manager.run()
