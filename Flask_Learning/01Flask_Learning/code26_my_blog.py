from flask import Flask
from code26_my_blog_admin import admin
app = Flask(__name__)
app.register_blueprint(admin)

# the homepage
@app.route('/')
def index():
    return "index page"


# the list of the blogs
@app.route("/list")
def list():
    return "list of the blogs"


# the specific page of the blogs
@app.route("/detail")
def detail():
    return "the detail"






if __name__ == "__main__":
    app.run()
