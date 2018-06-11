from flask import Flask,session

app = Flask(__name__)
app.config["SECRET_KEY"] = "AFDDJASJLFLDJFJIQWIEROFJDJF"
@app.route("/set_session")
def set_session():
    session["name"] = "python"
    return "set the session successfully"


@app.route("/get_session")
def get_session():
    name = session.get("name")
    return "get the session :"+ name
if __name__ == "__main__":
    app.run()