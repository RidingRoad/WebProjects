from flask import  Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('code15_custom_filter.html')


# the first method :decorator
@app.template_filter('custom_reverse')
def do_setup3(li):
    return li[::-1]
# the second method:app.add_template_filter(func_name,filter_name)
def do_setup2(li):
    return li[::-1]
app.add_template_filter(do_setup2,'func_reverse')


if __name__ == "__main__":
    app.run(debug=True)