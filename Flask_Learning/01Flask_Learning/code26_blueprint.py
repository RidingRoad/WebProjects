from flask import  Flask

from user import user_blue
app = Flask(__name__)
app.register_blueprint(user_blue)
# @app.route('/user')
# def user():
#     return "user"

@app.route('/news')
def news():
    return "news"

@app.route('/passport')
def passport():
    return  "passport"

@app.route("/")
def index():
    print(app.url_map)

    return "index page"


if __name__ == "__main__":

    app.run()
