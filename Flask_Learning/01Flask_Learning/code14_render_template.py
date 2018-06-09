from flask import  Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "name":"RidingRoad",
        "age":25,
        "city":"Mars",
        "my_custom_list":[1,2,3,4,5],
        "my_custom_dictionary":{"program":"Python"}
    }
    return render_template("code_14_template.html",template_data = data)


if __name__ == "__main__":
    app.run()