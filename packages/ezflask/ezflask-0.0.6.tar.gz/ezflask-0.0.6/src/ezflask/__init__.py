import flask
from markupsafe import escape

PNF = '<!DOCTYPE html><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. ' \
      'If you entered the URL manually please check your spelling and try again.</p> '


def _get_html(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return PNF


class EzFlask:
    def __init__(self):
        self.app = flask.Flask('')

        @self.app.route('/')
        def _index():
            return _get_html('index.html')

        @self.app.route('/<path>')
        def _get(path):
            return _get_html(escape(path))

        self.run()

    def run(self):
        self.app.run(host='0.0.0.0', port=8080)


EzFlask()
