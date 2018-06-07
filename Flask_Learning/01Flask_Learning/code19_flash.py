from flask import  Flask, flash,render_template

app = Flask(__name__)

class Config():
    SECRET_KEY = "SDASFDSAFSA"

app.config.from_object(Config)
@app.route('/')
def index():
    flash("input the user name:")
    flash("input the user email:")
    flash("input the user address:")
    flash("input the user phone:")
    return render_template('code_19_flash.html')


if __name__ == "__main__":
    app.run()