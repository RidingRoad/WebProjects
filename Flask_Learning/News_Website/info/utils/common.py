# 定义排行榜的根据索引进行匹配样式的过滤器
import functools

from flask import session, g

from info.models import User


def click_list_class_filter(index):
    if index == 0:
        return "first"
    elif index == 1:
        return "second"
    elif index == 2:
        return "third"
    else:
        return ""



# 装饰器封装用户登陆数据
def user_login_data(f):
    @functools.wraps(f)
    # 保证f.__name__ == 'f'
    def wrapper(*args,**kwargs):
        """ f.__name__ == wrapper.__name__"""
        user_id = session.get("user_id")
        user = None
        if user_id:
            # 如果能从session中获取到user_id,说明用户已经登录
            user = User.query.get(user_id)
        g.user = user
        return f(*args,**kwargs)
    return wrapper


