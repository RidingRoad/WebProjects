import random
import re
from flask import request, current_app, make_response, jsonify, session
from info import redis_store, constants, db
from info.models import User
from info.utils.captcha import captcha
from info.utils.response_code import RET
from info.utils.yuntongxun.sms import CCP
from . import passport_blue
from datetime import datetime


@passport_blue.route("/image_code")
def get_image_code():
    "获取图片验证码"
    # 获取当前图片的UUID编号
    image_code_id = request.args.get("code_id")
    # 生成验证码
    """
    generate_captcha()  Returns:
            A tuple, (name, text, StringIO.value).
            For example:
                ('fXZJN4AFxHGoU5mIlcsdOypa', 'JGW9', '\x89PNG\r\n\x1a\n\x00\x00\x00\r...')"""

    name, text, image = captcha.captcha.generate_captcha()
    try:
        # 保存当前图片生成的内容到redis中
        redis_store.set("ImageCodeId_"+image_code_id,text,constants.IMAGE_CODE_REDIS_EXPIRES)
        print("ImageCodeId_"+image_code_id)
        print(text)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(errno=RET.DATAERR,errmsg="保存图片验证码信息到redis服务器失败"))

    response = make_response(image)
    # 设置content-type
    response.headers["Content-Type"] = "image/jpeg"
    # 返回验证码图片到前端
    return response


@passport_blue.route("/sms_code",methods=["POST"])
def smscode():
    param_dict = request.json
    mobile = param_dict.get("mobile")
    # 用户输入的图片验证码
    image_code = param_dict.get("image_code")
    print("image_code",image_code)
    # 前端传过来的图片编码
    image_code_id = param_dict.get("image_code_id")
    print("image_code_id",image_code_id)
    # 检查参数是否有空
    if not all([mobile,image_code_id,image_code]):
        return jsonify(errno = RET.PARAMERR,errmsg= "参数不全")
    # 检查手机号码是否正确
    if not re.match(r"1[3456789]\d{9}$",mobile):
        return jsonify(errno=RET.DATAERR,errmsg="手机号不正确")

    # 如果上面都没问题,那么去校验图片验证码是否正确
    redis_image_code = redis_store.get("ImageCodeId_"+image_code_id)
    # 判断是否过期
    if not redis_image_code:
        return jsonify(errno=RET.NODATA,errmsg="图片验证码已过期")
    # 判断图片验证码是否正确
    if redis_image_code.lower() != image_code.lower():
        return jsonify(errno=RET.PARAMERR,errmsg="图片验证码错误")

    # 发送短信
    # 生成六位验证码
    result = random.randint(0,999999)
    sms_code = "%06d"%result
    print("短信验证码:"+sms_code)
    # 把验证码存储到redis中
    redis_store.set("sms_code_"+mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)


    # 发送短信验证码
    # status_code = CCP().send_template_sms(mobile,[sms_code,1],1)
    # if status_code !=0:
    #     return jsonify(errno=RET.THIRDERR,errmsg="短信发送失败")
    return jsonify(errno=RET.OK,errmsg="短信发送成功")


@passport_blue.route("/register",methods=["POST"])
def register():
    json_data = request.json
    mobile = json_data.get("mobile")
    sms_code = json_data.get("smscode")
    password = json_data.get("password")

    if not all([mobile,sms_code,password]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不全")

    # 校验短信验证码
    # 先校验是否过期
    try:
        redis_sms_code = redis_store.get("sms_code_"+mobile)
    except Exception as e :
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="获取redis手机验证码失败")

    if not redis_sms_code:
        return jsonify(errno=RET.NODATA, errmsg="短信验证码过期")

    if sms_code !=redis_sms_code:
        return jsonify(errno=RET.DATAERR, errmsg="短信验证码错误")
    try:
        redis_store.delete("sms_code_"+mobile)
    except Exception as e:
        current_app.logger.error(e)

    user = User()
    user.mobile = mobile
    user.nick_name = mobile
    user.password = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        # 数据保存错误
        return jsonify(errno=RET.DATAERR, errmsg="数据保存错误")
    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile

    # 6. 返回注册结果
    return jsonify(errno=RET.OK, errmsg="OK")


@passport_blue.route("/login",methods=['POST'])
def login():
    json_data = request.json
    mobile = json_data.get("mobile")
    password = json_data.get("password")

    # 判读是否为空
    if not all([mobile,password]):
        return jsonify(errno=RET.PARAMERR,errmsg="参数不全")

    # 去数据库查询用户是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR,errmsg="查询数据错误")

    if not user:
        return jsonify(errno=RET.USERERR,errmsg="用户不存在")

    # 验证密码
    if not user.check_password(password):
        return jsonify(errno=RET.PWDERR,errmsg="密码错误")

    # 保存用户登录状态
    session["user_id"] = user.id
    session["nick_name"] = user.nick_name
    session["mobile"] = user.mobile

    user.last_login = datetime.now()
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()

    return jsonify(errno=RET.OK,errmsg="登录成功")

@passport_blue.route("/logout",methods=["POST","GET"])
def logout():
    session.pop("user_id",None)
    session.pop("nick_name",None)
    session.pop("mobile",None)
    session.pop("is_admin",None)
    return jsonify(errno=RET.OK,errmsg="退出成功")


