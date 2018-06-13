from flask import Flask, current_app
# the current_app only can use to get the config (current_app.config.get(config_anme))

# initialize the flask and pass it an argument
app = Flask(__name__)

class Config():
    NAME = "RidingRoad"

app.config.from_object(Config)


# arguments limited to int
@app.route("/") # in the browser address directly append the float parameter after the "/"
def index():
    # response boby
    print(current_app.config.get("NAME"))
    return 'Hello Workd RidingRoad'


if __name__ == "__main__":
    # start the flask application
    app.run(debug=True)

    #
