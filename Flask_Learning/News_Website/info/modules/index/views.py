from info.models import User
from . import index_blue
from flask import current_app, render_template, session


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
            print(user.to_dict())
        except Exception as e:
            current_app.logger.error(e)

    return render_template("news/index.html",data={"user_info":user.to_dict() if user else None})


@index_blue.route("/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.ico")