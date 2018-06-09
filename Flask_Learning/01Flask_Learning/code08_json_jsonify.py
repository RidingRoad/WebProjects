from flask import Flask, json, jsonify



app = Flask(__name__)


@app.route('/json')
def demo():
    # response jsom format data to the client
    data = {
        "name":"RidingRoad",
        "age":'18'
    }
    # content = json.dumps(data)
    # return content,200,{"Content-Type":"application/json"}
    return jsonify(data) # recommend to use jsonify


if __name__ == "__main__":
    app.run()
