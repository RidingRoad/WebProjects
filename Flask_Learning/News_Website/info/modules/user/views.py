from flask import g, request, render_template, session, jsonify, redirect, current_app

from info.models import Category, News
from info.utils.image_storage import storage

from info import db, constants
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import profile_blue

@profile_blue.route("/info")
@user_login_data
def get_user_info():
    user = g.user
    if not user:
        return redirect('/')
    data = {
        "user_info":user.to_dict(),
    }
    return render_template("news/user.html",data=data)



@profile_blue.route("/base_info",methods=["GET","POST"])
@user_login_data
def base_info():
    user = g.user
    if request.method =="GET":
        data = {
            "user_info":user.to_dict() if user else None
        }
        return render_template("news/user_base_info.html",data=data)
    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender
    db.session.commit()
    session["nick_name"] = user.nick_name
    return jsonify(errno=RET.OK,errmsg="修改成功")

@profile_blue.route("/pic_info",methods=["GET","POST"])
@user_login_data
def pic_info():
    user = g.user
    if request.method =="GET":
        data = {
            "user_info":user.to_dict() if user else None
        }
        return render_template("news/user_pic_info.html",data=data)
    avatar_file = request.files.get("avatar").read()
    key = storage(avatar_file)
    user.avatar_url = key
    db.session.commit()
    data = {
        "avatar_url": constants.QINIU_DOMIN_PREFIX + key
    }

    return jsonify(errno=RET.OK,errmsg="上传成功",data=data)


@profile_blue.route("/pass_info",methods=["POST","GET"])
@user_login_data
def pass_info():
    if request.method == "GET":
        return render_template("news/user_pass_info.html")
    old_password = request.json.get("old_password")
    new_password = request.json.get("new_password")
    user = g.user
    if not user.check_password(old_password):
        return jsonify(errno=RET.PARAMERR,errmsg="密码有误")
    user.password = new_password
    db.session.commit()
    return jsonify(errno=RET.OK,errmsg="修改成功")

@profile_blue.route("/collection")
@user_login_data
def collection():
    page = request.args.get("p",1)
    try:
        page = int(page)
    except Exception as e :
        current_app.logger.error(e)
        page = 1

    user = g.user
    paginate = user.collection_news.paginate(page,5,False)
    items = paginate.items
    current_page = paginate.page
    total_page = paginate.pages
    collections = []
    for item in items:
        collections.append(item.to_dict())

    data = {
        "collections":collections,
        "current_page":current_page,
        "total_page":total_page
    }
    return render_template("news/user_collection.html",data=data)


@profile_blue.route("/news_release",methods=["POST",'GET'])
@user_login_data
def news_release():
    if request.method == "GET":
        category_list = Category.query.all()
        categories = []
        for category in category_list:
            categories.append(category.to_dict())
        categories.pop(0)
        data = {"categories":categories}
        return render_template("news/user_news_release.html",data=data)
    title = request.form.get("title")
    category_id = request.form.get("category_id")
    digest = request.form.get("digest")
    index_image = request.files.get("index_image")
    content = request.form.get("content")
    if not all([title,category_id,digest,index_image,content]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数输入错误")

    index_image = index_image.read()
    key = storage(index_image)
    user = g.user
    news = News()
    news.title = title
    news.source = "个人来源"
    news.digest = digest
    news.content = content
    news.index_image_url = constants.QINIU_DOMIN_PREFIX + key
    news.category_id = category_id
    news.user_id = user.id

    # 1 表示审核中
    news.status = 1
    db.session.add(news)
    db.session.commit()
    return jsonify(errno=RET.OK,errmsg="发布成功")

@profile_blue.route("/news_list")
@user_login_data
def news_list():
    page = request.args.get("p",1)
    try:
        page = int(page)
    except Exception as e:
        current_app.logger.error(e)
    user = g.user
    paginate = news = News.query.filter_by(user_id=user.id).paginate(page,10,False)
    items = paginate.items
    total_page = paginate.pages
    current_page = paginate.page

    news_release_list = []
    for item in items:
        news_release_list.append(item.to_review_dict())

    data = {
        "news_list":news_release_list,
        "current_page":current_page,
        "total_page":total_page
    }

    return render_template("news/user_news_list.html",data=data)



























