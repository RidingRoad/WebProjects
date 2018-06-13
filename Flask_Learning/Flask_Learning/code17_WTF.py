from flask import Flask,render_template,request

from flask_wtf import FlaskForm

from wtforms import StringField,PasswordField,SubmitField,
from wtforms.validators import DataRequired,EqualTo

app = Flask(__name__)

app.config["SECRET_KEY","jjjdaldjaladladjdsjafdsjk"]


class RegisterForm(FlaskForm):
    user_name = StringField(label="user:",validators=[DataRequired('must input user name')])
    password = PasswordField(label="pwd",validators=[DataRequired('must input password')])
    password2 = PasswordField(label="affirm pwd",validators=[DataRequired('must input password'),EqualTo('password','must be identical')])
    submit = SubmitField(label="submit")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "GET":
        form = RegisterForm()
        return render_template('code17_WTF.html',form = form)

if __name__ == "__main__":
    app.run()