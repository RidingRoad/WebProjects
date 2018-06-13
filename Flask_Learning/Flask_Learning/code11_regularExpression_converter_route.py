from flask import  Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class LimitIntConverter(BaseConverter):
    regex = "[0-9]{5,11}"

app.url_map.converters["limitint"] = LimitIntConverter


@app.route('/demo/<limitint:input>')
def demo(input):
    return 'demo: %s' %input
#
# @app.route('/<float:input>')
# def float_input(input):
#     return 'float_input: %f' %input
#
# @app.route('/<int:input>')
# def int_input(input):
#     return 'int_input: %d' %input
#
# @app.route('/<path:input>')
# def path_input(input):
#     return 'path_input: %s' %input

# @app.route('/<any:input>')
# def any_input(input):
#     return 'any_input: %s' %input


if __name__ == "__main__":
    app.run()