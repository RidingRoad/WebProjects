from flask import Flask

app = Flask(__name__)

@app.before_first_request
def handler_before_first_request():
    print("handler_before_first_request")



@app.before_request
def handler_before_request():
    print("handler_before_request")



@app.after_request
def handler_after_request(response):
    print("handler_after_request")
    return response



@app.teardown_request
def handler_teardown_request(error):
    print("handler_teardown_request")



@app.route('/')
def index():
    print("index page")
    return "index page"


if __name__ == "__main__":
    app.run()