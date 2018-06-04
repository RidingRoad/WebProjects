from flask import Flask,current_app
#initialize the flask and pass it arguments, but always pass the first arguments __name__
app = Flask(__name__)
#ctrl + P : to show the arguments

class Config(object):
    # to start the debug model
    DEBUG = True
    #  to switch lower and upper:ctrl shift u
    HAHAHA = 'I am RidingRoad'

# app.config.from_object(Config)
app.config.from_pyfile('config.cfg')
@app.route("/")
def index():
    #response boby
    a = 1/0
    # current_app is the client of app
    print(current_app.config.get('HAHAHA'))
    return 'Hello Workd RidingRoad'



if __name__ == "__main__":
    print(app.url_map)
    #start the flask application
    app.run(port=8899)