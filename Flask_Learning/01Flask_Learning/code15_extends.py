from flask import  Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('code16_extends_son.html')


if __name__ == "__main__":
    app.run()