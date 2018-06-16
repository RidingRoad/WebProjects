import redis, logging
from logging.handlers import RotatingFileHandler

from flask_wtf.csrf import generate_csrf

from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_session import Session
from config import config



db = SQLAlchemy()
redis_store = None

def setup_log(config_name):
    # 在__init__.create_app(config_name)设置了日志的记录等级
    # 调试debug级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

def create_app(config_name):
    setup_log(config_name)
    # 创建flask对象
    app = Flask(__name__)

    # 添加参数到flask对象中
    app.config.from_object(config[config_name])

    # mysql数据库实例绑定
    db.init_app(app)

    # redis数据库实例的创建,Return a Redis client object
    global redis_store
    redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

    # 对flask对象开启CSRFProtect保护
    CSRFProtect(app)

    @app.after_request
    def after_request(response):
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token", csrf_token)
        return response

    # 导入Session以便把flask对象中的session数据存入redis数据库
    Session(app)

    # 主页蓝图注册到app中
    from info.modules.index import index_blue
    app.register_blueprint(index_blue)


    # 登录和注册蓝图注册到app中
    from info.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    # 新闻详情注册
    from info.modules.news import news_blue
    app.register_blueprint(news_blue)

    return app
