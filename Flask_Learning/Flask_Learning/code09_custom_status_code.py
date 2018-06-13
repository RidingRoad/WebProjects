from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'index page',404,{"Content-/type":"application/json","Content-Length":89}

if __name__ == "__main__":
    app.run()