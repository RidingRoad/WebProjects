from flask import Flask,request

app = Flask(__name__)


@app.route("/index",methods=['GET','POST'])
def index():
    # get the information from form
    request.form.get('name')
    request.form.get('age')
    # get the request arguments
    request.args.get('city')
    # get the json format data,return the string
    print(request.data)


    return "index page"

if __name__ == "__main__":
    app.run()