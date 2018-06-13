from flask import Flask

app = Flask(__name__)

@app.route('/demo1')
def demo():
    #return  response_body,status_code,response_header
    return 'demo1',6666

if __name__ == "__main__":
    app.run()