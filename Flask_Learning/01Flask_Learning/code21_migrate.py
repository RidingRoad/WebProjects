from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell,Manager
from flask_migrate import Migrate,MigrateCommand

app = Flask(__name__)

class Config():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_ECHO = True

app.config.from_object(Config)


db = SQLAlchemy(app)

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('xxx',MigrateCommand)

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





if __name__ == "__main__":


    manager.run()