from flask import  Flask,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    photo = request.files.get('pic')
    photo.save('/2.png')
    return 'get the file sucessfully'

if __name__ == "__main__":
    app.run()