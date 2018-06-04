from flask import Flask
#initialize the flask and pass it an argument
app = Flask(__name__)

@app.route("/")
def index():
    #response boby
    return 'Hello Workd RidingRoad'



if __name__ == "__main__":
    #start the flask application
    app.run(port='8888')