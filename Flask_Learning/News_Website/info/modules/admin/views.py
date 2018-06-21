import datetime
import time
from flask import g, render_template, request, session, redirect, url_for, current_app, jsonify


from info import db, constants
from info.models import User, News, Category
from info.utils.common import user_login_data
from info.utils.image_storage import storage
from info.utils.response_code import RET
from . import admin_blue


@admin_blue.route("/index")
@user_login_data
def admin_index():
    user = g.user
    if not user:
        return render_template("admin/login.html")

    return render_template("admin/index.html", user=user.to_dict())


@admin_blue.route("/login", methods=["POST", "GET"])
def admin_login():
    if request.method == "GET":
        user_id = session.get("user_id", None)
        is_admin = session.get("is_admin", False)
        if user_id and is_admin:
            return redirect(url_for("admin.admin_index"))
        return render_template("admin/login.html")
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter(User.mobile == username, User.is_admin == True).first()
    if not user:
        return render_template("admin/login.html", errmsg="用户不存在")
    if not user.check_password(password):
        return render_template("admin/login.html", errmsg="密码错误")
    session["user_id"] = user.id
    session["mobile"] = user.mobile
    session["nick_name"] = user.nick_name
    session["is_admin"] = user.is_admin
    return redirect(url_for("admin.admin_index"))


@admin_blue.route("/user_count")
def user_count():
    total_count = 0
    mon_count = 0
    day_count = 0

    sum_count = User.query.filter(User.is_admin == False).count()
    t = time.localtime()
    print(t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec,t.tm_wday,t.tm_yday,t.tm_isdst)
    mon_begin = "%d-%02d-01" % (t.tm_year, t.tm_mon)
    mon_begin_date = datetime.datetime.strptime(mon_begin, "%Y-%m-%d")
    mon_count = User.query.filter(User.is_admin == False, User.create_time > mon_begin_date).count()
    day_begin = "%d-%02d-%02d" % (t.tm_year, t.tm_mon, t.tm_mday)
    day_begin_date = datetime.datetime.strptime(day_begin, "%Y-%m-%d")
    day_count = User.query.filter(User.is_admin == False, User.create_time > day_begin_date).count()
    today_begin = "%d‐%02d‐%02d"%(t.tm_year,t.tm_mon, t.tm_mday)
    today_begin_date = datetime.datetime.strptime(day_begin, "%Y-%m-%d")
    activate_count = []
    activate_time = []
    for i in range(0, 31):
        begin_date = today_begin_date - datetime.timedelta(days=i)
        end_date = today_begin_date-datetime.timedelta(days=(i-1))
        count = User.query.filter(User.is_admin==False,User.create_time>=begin_date,User.create_time<end_date).count()
        activate_count.append(count)
        activate_time.append(begin_date.strftime("%Y-%m-%d"))
    activate_time.reverse()
    activate_count.reverse()
    data ={
        "total_count":sum_count,
        "mon_count":mon_count,
        "day_count":day_count,
        "activate_count":activate_count,
        "activate_time":activate_time
    }
    return render_template("admin/user_count.html", data=data)

@admin_blue.route("/user_list")
@user_login_data
def user_list():
    page = request.args.get("p",1)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1
    paginate = User.query.filter(User.is_admin==False).order_by(User.last_login.desc()).paginate(page,1,False)
    items = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    users = []
    for user in items:
        users.append(user.to_admin_dict())

    data = {
        "users":users,
        "current_page":current_page,
        "total_page":total_page
    }
    return render_template("admin/user_list.html", data=data)


@admin_blue.route("/news_review")
def news_review():
    page = request.args.get("p",1)
    keyswords = request.args.get("keyswords")
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    filters = [News.status==1]


    if keyswords:
            filters.append(News.title.contains(keyswords))

    paginate = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,10,False)
    items = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    news_list = []
    for item in items:
        news_list.append(item.to_review_dict())

    data = {
        "news_list":news_list,
        "current_page":current_page,
        "total_page":total_page
    }

    return render_template("admin/news_review.html",data=data)

@admin_blue.route("/news_review_detail",methods=["GET","POST"])
def news_review_detail():
    if request.method == "GET":
        news_id = request.args.get("news_id")
        news = News.query.get(news_id)
        data = {
            "news":news.to_dict()
        }
        return render_template("admin/news_review_detail.html",data=data)
    action = request.json.get("action")
    news_id = request.json.get("news_id")
    reason = request.json.get("reason")

    news = News.query.get(news_id)

    if action == "accept":
        news.status = 0
    else:
        if not reason:
            return jsonify(errno=RET.PARAMERR,errmsg="拒绝原因")
        news.status = -1
        news.reason = reason

    db.session.commit()
    return jsonify(errno=RET.OK, errmsg="操作成功")


@admin_blue.route("/news_edit")
def news_edit():
    page = request.args.get("p",1)
    keywords = request.args.get("keyswords",'')
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
        page = 1

    news_list = []
    current_page = 1
    total_page = 1

    try:
        filters = []
        if keywords:
            filters.append(News.title.contains(keywords))
        paginate  = News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,constants.ADMIN_NEWS_PAGE_MAX_COUNT,False)
        news_list = paginate.items
        current_page = paginate.page
        total_page = paginate.pages
    except Exception as e:
        current_app.logger.error(e)

    news_dict_list = []
    for news in news_list:
        news_dict_list.append(news.to_basic_dict())

    data = {
        "total_page":total_page,
        "current_page":current_page,
        "news_list":news_dict_list
    }

    return render_template("admin/news_edit.html",data=data)


@admin_blue.route("/news_edit_detail",methods=["POST","GET"])
def news_edit_detail():
    if request.method == "GET":
        news_id = request.args.get("news_id")
        if not news_id:
            return render_template("admin/news_edit_detail.html",data={"errmsg":"新闻ID缺失"})
        news = None
        try:
            news = News.query.get(news_id)
        except Exception as e:
            current_app.logger.error(e)
        if not news:
            return render_template("admin/news_edit_detail.html",data={"errmsg":"没有此新闻"})
        categories = Category.query.all()
        categories_list = []
        for category in categories:
            category_dict = category.to_dict()
            category_dict["is_selected"]=False
            if category.id == news.category_id:
                # 默认显示原来的分类
                category_dict["is_selected"] = True
            categories_list.append(category_dict)
        categories_list.pop(0)

        data = {
            "news":news.to_dict(),
            "categories":categories_list,

        }

        return render_template("admin/news_edit_detail.html",data=data)


    news_id = request.form.get("news_id",'')
    if not news_id:
        return jsonify(errno=RET.PARAMERR,errmsg="news_id参数有误")

    title = request.form.get("title")
    if not title:
        return jsonify(errno=RET.PARAMERR,errmsg="title参数有误")
    digest = request.form.get("digest")
    if not digest:
        return jsonify(errno=RET.PARAMERR,errmsg="digest参数有误")
    content = request.form.get("content")
    if not content:
        return jsonify(errno=RET.PARAMERR,errmsg="content参数有误")
    index_image = request.files.get("index_image")
    if not index_image:
        return jsonify(errno=RET.PARAMERR,errmsg="index_image参数有误")
    category_id = request.form.get("category_id")
    if not category_id:
        return jsonify(errno=RET.PARAMERR,errmsg="category_id参数有误")
    if not all([news_id,title,digest,content,index_image,category_id]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.NODATA,errmsg="没有此新闻")
    if index_image:
        try:
            index_image = index_image.read()

        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.PARAMERR,errmsg="图片有误")
        try:
            key = storage(index_image)
        except Exception as e :
            current_app.logger.error(e)
            return jsonify(errno=RET.THIRDERR,errmsg="上传图片错误")
        news.index_image_url = constants.QINIU_DOMIN_PREFIX + key

    news.title = title
    news.digest = digest
    news.content = content
    news.category_id = category_id


    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="数据保存失败")
    return jsonify(errno=RET.OK,errmsg="编辑成功")

@admin_blue.route('/news_type')
def get_news_type():
    categories = Category.query.all()
    categories_dicts = []
    for category in categories:
        category_dict = category.to_dict()
        categories_dicts.append(category_dict)

    categories_dicts.pop(0)
    data = {
        "categories":categories_dicts
    }
    return render_template("admin/news_type.html",data=data)

@admin_blue.route("/add_category",methods=["POST"])
def add_category():
    category_id = request.json.get("id")
    category_name = request.json.get("name")
    if not category_name:
        return jsonify(errno=RET.PARAMERR,errmsg="参数错误")
    if category_id:
        try:
            category = Category.query.get(category_id)
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=RET.DBERR,errmsg="查询数据失败")

        if not category:
            return jsonify(errno=RET.NODATA,errmsg="没有此分类信息")
        category.name = category_name
    else:
        category = Category()
        category.name = category_name
        db.session.add(category)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="保存数据失败")
    return jsonify(errno=RET.OK,errmsg="保存数据成功")














