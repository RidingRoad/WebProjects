from flask import render_template, make_response

from . import news_blue


@news_blue.route("/<int:news_id>")
def news_detail(news_id):
    print(news_id)
    return "hahaha"
    # return render_template("news/detail.html")
