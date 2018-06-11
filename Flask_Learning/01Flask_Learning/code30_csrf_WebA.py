import base64
import os
from _curses import flash

from flask import Flask, render_template, make_response
from flask import redirect
from flask import request
from flask import url_for

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # 取到表单中提交上来的参数
        username = request.form.get("username")
        password = request.form.get("password")

        if not all([username, password]):
            # all() if every element in the sequence is bool(x)==True or sequence is empty,then return True
           print('参数错误')
        else:
            print(username, password)
            if username == 'laowang' and password == '1234':
                # 状态保持，设置用户名到cookie中表示登录成功
                response = redirect(url_for('transfer'))
                response.set_cookie('username', username)
                return response
            else:
                print('密码错误')

    return render_template('temp_login.html')


@app.route('/transfer', methods=["POST", "GET"])
def transfer():
    # 从cookie中取到用户名
    username = request.cookies.get('username', None)
    # 如果没有取到，代表没有登录
    if not username:
        return redirect(url_for('index'))

    if request.method == "POST":
        to_account = request.form.get("to_account")
        money = request.form.get("money")
        # 取到表单中的token
        form_csrf_token = request.form.get('csrf_token')
        # cookie中的token
        cookie_csrf_token = request.cookies.get('csrf_token', "")

        # 做校验。如果校验成功，再进行转账逻辑
        if form_csrf_token != cookie_csrf_token:
            return "非法请求"

        print('假装执行转账操作，将当前登录用户的钱转账到指定账户')
        return '转账 %s 元到 %s 成功' % (money, to_account)

    csrf_token = generate_csrf()
    # 渲染转换页面
    response = make_response(render_template('temp_transfer.html', csrf_token=csrf_token))
    # response = make_response(render_template('temp_transfer.html'))
    # 往cookie中添加csrf_token
    response.set_cookie('csrf_token', csrf_token)
    return response


# 生成 csrf_token
def generate_csrf():
    return bytes.decode(base64.b64encode(os.urandom(48)))


if __name__ == '__main__':
    app.run(debug=True, port=9000)