# 配置项目参数
import redis, logging

class Config(object):

    # 添加mysql数据库的配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:mysql@127.0.0.1:3306/news_website"
    SQLALCHEMY_TRACK_MODIFICATION = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 添加redis数据库的配置信息
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379
    # 配置Session
    # 使用session必须配置SECRET_SKY，可以使用加密的或者自定义，建议实际项目中使用UUID
    SECRET_KEY = "DDAJDJFQIOWEOWQOQOPTPOFDSJJGJQJJJFJASDJFQIUJAFDAD"
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIM = 3600*24*2
    # SESSION_REDIS这里不能加deconde_response=True,因为session是在内存中与redis进行交互的
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT) # Return a Redis client object



class DevelopmentConfig(Config):
    """调试模式下的app"""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    """生产模式下的app"""
    DEBUG = False
    LOG_LEVEL = logging.ERROR

config = {
    "production":ProductionConfig,
    "development":DevelopmentConfig
}


