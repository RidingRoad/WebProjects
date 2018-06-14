import random
import re

import datetime

from flask import current_app
from flask import make_response
from flask import request, jsonify
from flask import session

from info.models import User
from info import constants, db
from info import redis_store
from info.utils.yuntongxun.sms import CCP
from . import passport_blue
from info.utils.response_code import RET
from info.utils.captcha.captcha import captcha


@passport_blue.route("/logout")
def logout():
    session.pop("user_id",None)
    session.pop("mobile",None)
    session.pop("nick_name",None)
    return jsonify(errno=RET.OK,errmsg="logout successfully")


@passport_blue.route("/register", methods=["POST"])
def register():
    mobile = request.json.get("mobile")
    smscode = request.json.get("smscode")
    password = request.json.get("password")

    if not all([mobile, smscode, password]):
        return jsonify(errno=RET.PARAMERR, errmsg="parameters eror")

    redis_sms_code = redis_store.get("code_" + mobile)
    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="expired")

    if redis_sms_code != smscode:
        return jsonify(errno=RET.PARAMERR, errmsg="error sms_code")

    user = User()
    user.mobile = mobile
    user.nick_name = mobile
    user.password = password
    user.last_login = datetime.datetime.now()

    try:
        db.seesion.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile
    return jsonify(errno=RET.OK, errmsg="register successfully")


@passport_blue.route("/login", methods=["POST"])
def login():
    mobile = request.json.get("mobile")
    password = request.json.get("password")

    user = User.query.filter(User.mobile == mobile).first()
    if not user:
        return jsonify(errno=RET.NODATA, errmsg="no this user")
    if not user.check_password(password):
        return jsonify(errno=RET.PARAMERR, errmsg="error password")
    session['user_id'] = user.id
    session['mobile'] = user.mobile
    session['nick_name'] = user.nick_name
    user.last_login = datetime.datetime.now()
    db.session.commit()
    return jsonify(errno=RET.OK, errmsg="login successfully")


@passport_blue.route("/sms_code", methods=["POST"])
def sms_code():
    print(1)
    mobile = request.json.get("mobile")
    print(mobile)
    image_code = request.json.get("image_code")
    print(image_code)
    image_code_id = request.json.get("image_code_id")
    print(image_code_id)
    if not all([mobile, image_code, image_code_id]):
        return jsonify(errno=RET.PARAMERR, errmsg="input the data")
    if not re.match("1[3456789]\d{9}", mobile):
        return jsonify(errno=RET.PARAMERR, errmsg="input the right mobile")
    redis_image_code = redis_store.get("sms_code_" + image_code_id)
    print(redis_image_code)
    if not redis_image_code:
        return jsonify(errno=RET.PARAMERR, errmsg="expired")

    if redis_image_code != image_code:
        return jsonify(errno=RET.PARAMERR, errmsg="input right captcha")
    result = random.randint(0, 999999)
    sms_code = "%06d" % result
    redis_store.set("code_" + mobile, sms_code, 300)
    statusCode = CCP().send_template_sms(mobile, [sms_code, 1], 1)

    if statusCode:
        return jsonify(errno=RET.THIRDERR, errmsg="sms_code send error")
    return jsonify(errno=RET.OK, errmsg="successfully sent sms_code")


@passport_blue.route("/image_code")
def image_code():
    # get the code_id from the front
    print("the request from the front,url:" + request.url)
    code_id = request.args.get("code_id")

    if not code_id:
        return jsonify(errno=RET.PARAMERR, errmsg="parameters error")

    # get the picture  verification code
    name, text, image = captcha.generate_captcha()
    print("picture verification code:" + text)
    # save the uuid into the redis
    redis_store.set("sms_code_" + code_id, text, constants.SMS_CODE_REDIS_EXPIRES)
    response = make_response(image)
    return response
