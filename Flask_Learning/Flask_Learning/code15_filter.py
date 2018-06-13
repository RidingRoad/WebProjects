from flask import  Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('code15_filter.html')

def do_setup2(li):
    return li[::2]

@app.template_filter('slice3')
def do_setup3(li):
    return li[::3]

app.add_template_filter(do_setup2,'slice2')


if __name__ == "__main__":
    app.run()