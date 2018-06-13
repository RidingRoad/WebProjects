from flask import Flask

#initialize the flask and pass it an argument
from flask import request

app = Flask(__name__)
# PAGE :CTRL ALT O
# IMPORT : ALT ENTER
@app.route("/",methods=['GET','POST'])
def index():
    #response boby
    if request.method =='GET':
        print("in get method")
    if request.method =='POST':
        print("in post method")
    return 'request successfully'



if __name__ == "__main__":
    #start the flask application
    app.run()