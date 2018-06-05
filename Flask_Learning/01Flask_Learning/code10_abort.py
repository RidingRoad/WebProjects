from flask import Flask, abort

app = Flask(__name__)

# ctrl + j
@app.route('/')
def index():
    print("XiaoMi8")
    print("XiaoMi7")
    abort(404)
    # return "index page"
    print("XiaoMi6")


@app.errorhandler(404)
def handler_404_error(err):
    return "can not find the page%s"%err


if __name__ == "__main__":
    app.run()