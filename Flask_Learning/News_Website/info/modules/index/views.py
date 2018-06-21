from info import constants
from info.models import User, News, Category
from flask import current_app, render_template, session, request, jsonify

from info.utils.response_code import RET
from . import index_blue


@index_blue.route("/index")
def index():
    return render_template("news/index.html")

@index_blue.route("/")
def index_null():
    user_id = session.get("user_id")
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
            # print("user:",user)
            # print("user.to_dict:",user.to_dict())
        except Exception as e:
            current_app.logger.error(e)

    # 获取排行数据
    news_list = []
    try:
        news_list = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS)
        # print("news_list_10:",news_list)
        """news_list_10: SELECT info_news.create_time AS info_news_create_time, info_news.update_time AS info_news_update_time, info_news.id AS info_news_id, info_news.title AS info_news_title, info_news.source AS info_news_source, info_news.digest AS info_news_digest, info_news.content AS info_news_content, info_news.clicks AS info_news_clicks, info_news.index_image_url AS info_news_index_image_url, info_news.category_id AS info_news_category_id, info_news.user_id AS info_news_user_id, info_news.status AS info_news_status, info_news.reason AS info_news_reason FROM info_news ORDER BY info_news.clicks DESC LIMIT %s"""
        # print("type(news_list_10):", type(news_list)) # type(news_list_10): <class 'flask_sqlalchemy.BaseQuery'>
    except Exception as e:
        current_app.logger.error(e)

    click_news_list = []
    for news in news_list if news_list else []:
        click_news_list.append(news.to_basic_dict())
    # print("click_news_list:",click_news_list)
    """
    click_news_list: 
    [{'id': 4551, 'title': '华尔街见闻早餐FM-Radio|2018年1月11日', 'source': '张舒', 'digest': '①标普纳指年内首跌，但银行股', 'create_time': '2018-01-11 07:01:17', 'index_image_url': 'https://wpimg.wallstcn.com/164cf47b-057c-41ad-b558-54c944054e49.png', 'clicks': 211}, ......]

    """


    # 获取新闻首页分类,并默认显示第一个分类
    categories = Category.query.all()
    categories_dicts = []
    # Categoried: [<Category 1>, <Category 2>, <Category 3>, <Category 4>, <Category 5>, <Category 6>]
    for index,category in enumerate(categories):
        # print(index,category)
        """
        (0, <Category 1>)
        (1, <Category 2>)
        (2, <Category 3>)
        (3, <Category 4>)
        (4, <Category 5>)
        (5, <Category 6>)
        """
        categories_dicts.append(category.to_dict())
        # print(category.to_dict())

    data = {"user_info": user.to_dict() if user else None, "click_news_list": click_news_list,"categories":categories_dicts}

    return render_template("news/index.html",data=data)


@index_blue.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.ico")


# 获取首页新闻分页,根据前端需求的哪个分类(cid),第几页(p)和每页的新闻条数(per_page)按需求返回
@index_blue.route("/news_list")
def get_news_list():
    args_dict = request.args # 获取get请求中的参数127.0.0.1/5000/newslist?&cid=2&page=2&per_page=10
    page = args_dict.get("page","1") # 不传默认为1
    per_page = args_dict.get("per_page",constants.HOME_PAGE_MAX_NEWS) # 不传默认为constants.HOME_PAGE_MAX_NEWS
    category_id = args_dict.get("cid","1") # 不传的话默认分类为1

    try:
        page = int(page)  # 以防数据类型不对,进行转换以免发送后续的语法报错
        per_page = int(per_page)
        category_id = int(category_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")

    filters = [News.status==0]  # 存放指定分类的对象
    if category_id != 1:
        # 把分类对象放入到列表中
        filters.append(News.category_id==category_id)
        # News.category_id==category_id 返回的是News模型里面符合与category_id的值相等的所有对象
    try:
        # page ,获取第几页,页数
        # per_page 每页返回多少条数据,每一页的项目数，这里也就是说每一页显示的新闻条数
        # 错误标志。如果是 True，当请求的范围页超出范围的话，一个 404 错误将会自动地返回到客户端的网页浏览器。如果是 False，返回一个空列表而不是错误。
        paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,True)
        # paginate(page,per_page,True)  return Pagination(self, page, per_page, total, items)
        # page : 第几页
        # per_page : 每页的数据条数
        # items : page页对应的数据item对象列表
        # News.query.filter(News.category_id == category_id).order_by(News.create_time.desc()) 获得这个类别的按最新时间降序的所有文章
        items = paginate.items  # 一个页面的per_page条数据对象
        # print(type(items))
        # print(items)
        # [<News 4619>, <News 3469>, <News 3489>, <News 3485>, <News 3504>, <News 3502>, <News 3513>, <News 3528>, <News 3515>, <News 3524>]
        total_page = paginate.pages
        current_page = paginate.page
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据查询失败")
    news_list =  []
    for news in items:
        news_list.append(news.to_basic_dict())
    data = {
        "total_page":total_page,"current_page":current_page,"news_list":news_list,"cid":category_id}

    return jsonify(errno=RET.OK,errmsg="OK",data = data)

