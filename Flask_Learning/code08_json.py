from flask import Flask, jsonify



app = Flask(__name__)


@app.route('/demo')
def demo():

    data = {
        "name":"zhang",
        "age":'18'
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()
