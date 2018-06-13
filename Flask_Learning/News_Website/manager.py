from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
# import sys
from info import create_app,db, models

"""
manager:只是负责启动当前应用程序


"""
app = create_app("development")
manager = Manager(app)
Migrate(app,db)
manager.add_command("mysql",MigrateCommand)


if __name__ == '__main__':
    print(app.url_map)
    # print(sys.path)
    manager.run()