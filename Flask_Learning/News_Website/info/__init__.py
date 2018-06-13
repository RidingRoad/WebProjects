import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from config import config_map, DevelopmentConfig, ProductionConfig
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# 如下设置日志是固定的写法(大家直接拷贝)
# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024, backupCount=20)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger().addHandler(file_log_handler)

redis_store = None  # type:redis.StrictRedis

db = SQLAlchemy()


# 创建并且返回flask对象
def create_app(config_name):
    """
    create and return the flask object
    """
    app = Flask(__name__)
    # 在不动当前代码的同时,修改config类的名字
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)
    # 数据库需要在app加载config文件之后执行,不然会直接报一个警告
    db.init_app(app)
    # 初始化redis的存储数据对象(短信验证码,图片验证码)
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST, port=config_class.REDIS_PORT, decode_responses=True)

    Session(app)
    # 开启CSRF保护
    CSRFProtect(app)
    # 在需要导入模块的时候,才import
    from info.index import index_blue
    app.register_blueprint(index_blue)

    from info.passport import passport_blue
    app.register_blueprint(passport_blue)
    return app
