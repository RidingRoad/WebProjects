from flask import Flask, request, render_template
from flask import flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "asdfjdsfjqopewqotnfasfdngsa"


@app.route('/demo1', methods=["POST", "GET"])
def demo1():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not all([username, password, password2]):
            flash("params not enough")
            return render_template("code17_html_forms_register.html")
        elif password2 != password:
            flash("the password is not the same")
            return render_template("code17_html_forms_register.html")
        else:
            print(username, password, password2)
            return "successfully register,%s" % username
    if request.method == "GET":
        return render_template("code17_html_forms_register.html")


if __name__ == "__main__":
    app.run(debug=True)
