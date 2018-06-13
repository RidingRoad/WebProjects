from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/demo1')
def demo1():
    return 'I am demo1'

@app.route('/demo2')
def demo2():
    return redirect(url_for('demo1'))


if __name__ == "__main__":
    app.run()