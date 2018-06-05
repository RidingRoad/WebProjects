from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        "name":'python',
        "city":'sz',
        "my_ul":[1,2,3,4],
        "my_dict":{'age':18}
    }

    return render_template("code_14_template.html",data_obj = data)

if __name__ == "__main__":
    app.run()