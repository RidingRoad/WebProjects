from flask import Flask, make_response,request

app = Flask(__name__)

@app.route('/baidu')
def set_cookie():
    resp = make_response("set cookie to the browser")
    resp.set_cookie("pwd","123",max_age=3600)
    resp.set_cookie("city","sz")
    return resp

@app.route("/get_cookie")
def get_cookie():
    name = request.cookies.get("pwd")
    return "get the cookie successfully:"+ name

if __name__ == "__main__":
    app.run()