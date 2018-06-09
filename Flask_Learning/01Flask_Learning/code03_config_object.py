# to know how to config the flask app  by object
from flask import Flask
#initialize the flask and pass it arguments, but always pass the first arguments __name__
app = Flask(__name__)
#ctrl + P : to show the arguments

class Config(object):
    # to start the debug model
    DEBUG = True

app.config.from_object(Config)

@app.route("/")
def index():
    #response boby
    a = 1/0 # it will raise the ZeroDivisionError
    return 'Hello Workd RidingRoad'



if __name__ == "__main__":
    # print(app.url_map)
    #start the flask application
    app.run()