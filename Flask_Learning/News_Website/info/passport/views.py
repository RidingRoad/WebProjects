from flask import make_response
from flask import request, jsonify


from info import constants
from info import redis_store
from . import passport_blue
from info.utils.response_code import RET
from info.utils.captcha.captcha import captcha


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
    redis_store.set("sms_clde_" + code_id, text, constants.SMS_CODE_REDIS_EXPIRES)
    response = make_response(image)
    return response
