from flask import Flask, request


class Router:
    def __init__(self):
        self.app = Flask(__name__)

    def run_server(self):
        self.app.run(debug=True)

    def user(self):
        self.__app.add_url_rule()
        html = f"<h1>User</h1>"
        return html