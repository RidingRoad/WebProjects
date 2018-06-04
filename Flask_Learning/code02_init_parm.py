from flask import Flask
#initialize the flask and pass it arguments, but always pass the first arguments __name__
app = Flask(__name__)
#ctrl + P : to show the arguments
@app.route("/")
def index():
    #response boby
    return 'Hello Workd RidingRoad'



if __name__ == "__main__":
    print(app.url_map)
    #start the flask application
    app.run()