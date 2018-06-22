from flask import render_template, make_response, g, jsonify, request, current_app

from info import db
from info.models import News, Comment, CommentLike, User
from info.utils.common import user_login_data
from info.utils.response_code import RET
from . import news_blue


@news_blue.route("/<int:news_id>")
@user_login_data
def news_detail(news_id):
    user = g.user
    """查询右边热门新闻的数据"""
    news_model = News.query.order_by(News.clicks.desc()).limit(10)
    news_clicks = []
    for news in news_model:
        news_clicks.append(news.to_dict())

    """根据新闻ID查询当前新闻详情里面的数据"""
    news = News.query.get(news_id)
    # 点击量加一
    news.clicks += 1



    """收藏新闻"""
    is_collection = False
    is_followed = False
    if user:
        if news in user.collection_news:
            is_collection = True
    if news.user and user:
        if news.user in user.followed:
            is_followed = True




    # 获取评论
    comments = Comment.query.filter(Comment.news_id==news_id).all()
    comment_list = []
    for item in comments:
        comment_list.append(item.to_dict())

    """获取新闻的评论信息"""
    comments = Comment.query.filter(Comment.news_id==news_id).all()
    comment_likes = []
    comment_like_ids = []
    if user:
        comments_list = CommentLike.query.filter(CommentLike.user_id==user.id).all()
        comment_like_ids = [comment_like.comment_id for comment_like in comment_likes]
    comments_list = []
    for item in comments:
        item_dict = item.to_dict()
        item_dict["is_like"] = False
        if item.id in comment_like_ids:
            item_dict["is_like"] = True
        comments_list.append(item_dict)



    data = {
        "user_info": user.to_dict() if user else None,
        "click_news_list": news_clicks,
        "news": news.to_dict(),
        "is_collected": is_collection,
        "comments":comments_list,
        "is_followed":is_followed
    }
    return render_template("news/detail.html", data=data)

@news_blue.route("/news_collect",methods=["POST"])
@user_login_data
def news_collect():
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR,errmsg="请登录")
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    news = News.query.get(news_id)

    if not news:
        return jsonify(errno=RET.NODATA,errmsg="没有此数据")
    if action == "collect":
        user.collection_news.append(news)
    else:
        user.collection_news.remove(news)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
    return jsonify(errno=RET.OK,errmsg="收藏成功")


@news_blue.route("/news_comment",methods=["POST"])
@user_login_data
def news_comment():
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR,errmsg="请登录")
    news_id = request.json.get("news_id")
    comment_str = request.json.get("comment")
    parent_id = request.json.get("parent_id")

    news = News.query.get(news_id)
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_str
    if parent_id:
        comment.parent_id = parent_id

    db.session.add(comment)
    db.session.commit()

    return jsonify(errno=RET.OK,errmsg="评论成功",data=comment.to_dict())




@news_blue.route("/comment_like",methods=["POST"])
@user_login_data
def comment_like():
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR,errmsg="请登录")
    comment_id = request.json.get("comment_id")
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    comment = Comment.query.get(comment_id)
    if action == "add":
        comment_like = CommentLike.query.filter_by(comment_id=comment_id,user_id = user.id).first()
        if not comment_like:
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = user.id
            db.session.add(comment_like)

            comment.like_count += 1
            db.session.commit()

    else:
        comment_like = CommentLike.query.filter_by(comment_id = comment_id,user_id = user.id).first()
        if comment_like:
            db.session.delete(comment_like)
            comment.like_count -= 1
            db.session.commit()
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR,errmsg="操作失败")
    return jsonify(errno=RET.OK,errmsg="操作成功")



@news_blue.route("/followed_user",methods=["POST"])
@user_login_data
def followed_user():
    if not g.user:
        return jsonify(errno=RET.SESSIONERR,errmsg="未登录")
    user_id = request.json.get("user_id")
    action = request.json.get("action")

    if not all([user_id,action]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")
    if action not in ("follow","unfollow"):
        return jsonify(errno=RET.PARAMERR,errmsg="action参数错误")
    try:
        target_user=User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据库查询失败")
    if not target_user:
        return jsonify(errno=RET.NODATA,errmsg="未查询到用户数据")
    if action == "follow":
        if target_user.followers.filter(User.id==g.user.id).count()>0:
            return jsonify(errno=RET.DATAEXIST,errmsg="已关注")
        target_user.followers.append(g.user)
    else:
        if target_user.followers.filter(User.id==g.user.id).count()>0:
            target_user.followers.remove(g.user)

    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="数据保存错误")
    return jsonify(errno=RET.OK,errmsg="操作成功")






