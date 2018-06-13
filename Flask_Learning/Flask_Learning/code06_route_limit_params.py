from flask import Flask

# initialize the flask and pass it an argument
app = Flask(__name__)


# arguments limited to int
@app.route("/demo/<float:user_id>") # in the browser address directly append the float parameter after the "/"
def index(user_id):
    # response boby
    return 'Hello Workd RidingRoad %f' % user_id


if __name__ == "__main__":
    # start the flask application
    app.run()

    #
