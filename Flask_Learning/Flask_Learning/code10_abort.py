from flask import Flask, abort

app = Flask(__name__)

@app.route('/666')
def index():
    print(1234)
    print(1234)
    abort(404)
    # return "index page"
    print(1234)

@app.errorhandler(404)
def error_404_handler(error_code):
    return "the server had moved out to Mars"


if __name__ == "__main__":
    app.run()