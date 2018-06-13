from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo
from wtforms import StringField, SubmitField, PasswordField

app = Flask(__name__)
app.config["SECRET_KEY"] = "afhwqutewtufujasdnnvajsfhdsaio"


class RegisterForm(FlaskForm):
    user_name = StringField(label="user name:", validators=[DataRequired("must input")])
    password = PasswordField(label="password:", validators=[DataRequired("must input")])
    confirm_password = PasswordField(label="confirm password:", validators=[DataRequired("must input"),
                                                                            EqualTo("password",
                                                                                    "must be same to the above password")])
    submit = SubmitField(label="submit")


@app.route('/register', methods=["GET", "POST"])
def register():
    register_form_end = RegisterForm()
    if request.method == "GET":
        return render_template("code17_WTF.html", register_form_front = register_form_end)
    if request.method == "POST":
        if register_form_end.validate_on_submit():
            return "register successfully"
        else:
            return render_template("code17_WTF.html",register_form_front = register_form_end)


if __name__ == "__main__":
    app.run()
