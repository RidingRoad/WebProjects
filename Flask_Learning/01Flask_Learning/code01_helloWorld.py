# to primaryly know the flask work_flows
from flask import Flask
#initialize the flask and pass it an argument
app = Flask(__name__)

@app.route("/")
def index():
    #response boby
    return 'Hello Workd RidingRoad'



if __name__ == "__main__":
    #start the flask application
    print(app.url_map)
    app.run(debug=True)