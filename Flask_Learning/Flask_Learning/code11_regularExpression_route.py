from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    regex = '[0-9]{3}'

app.url_map.converters['custom'] = RegexConverter
@app.route('/demo/<custom:user_id>')
def demo(user_id):
    #return  response_body,status_code,response_header
    return 'demo=%s'%user_id

if __name__ == "__main__":
    app.run()