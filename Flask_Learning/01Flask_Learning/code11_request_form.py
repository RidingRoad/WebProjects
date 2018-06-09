from flask import  Flask, request

app = Flask(__name__)

@app.route('/index',methods=["GET","POST"])
def index():
    name = request.form.get("name")
    age = request.form.get("age")
    city = request.form.get("city")
    gender = request.args.get("gender")
    pic = request.files.get("pic")
    pic.save('./receive.png')
    return "name = %s, age = %s , city = %s, gender = %s,pic is successfuly sent" %(name,age,city,gender)

if __name__ == "__main__":
    app.run()