from  flask  import  Flask, render_template,g
from flask import flash

app = Flask(__name__)
app.config["SECRET_KEY"]=True

@app.route('/')
def index():
    g.name = "RidingRoad"
    my_list = [
        {
            "id": 1,
            "value": "我爱工作"
        },
        {
            "id": 2,
            "value": "工作使人快乐"
        },
        {
            "id": 3,
            "value": "沉迷于工作无法自拔"
        },
        {
            "id": 4,
            "value": "日渐消瘦"
        },
        {
            "id": 5,
            "value": "以梦为马，越骑越傻"
        }
    ]
    flash("1")
    flash("2")
    flash("3")
    flash("4")
    flash("5")
    flash("6")
    return render_template('code_18_control.html',my_list=my_list)


if __name__ == "__main__":
    app.run(debug=True)