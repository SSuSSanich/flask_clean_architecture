from flask import Flask, request, render_template, redirect, abort, Response

from blueprint.admin_page import admin_page
from blueprint.errorhandler import errorhandler
from blueprint.index_page import index_page
from blueprint.login_page import login_page, login_manager
from blueprint.sign_up_page import sign_up_page
from blueprint.user_page import user_page

from config import FLASK_SECRET_KEY

app = Flask(__name__)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY

app.register_blueprint(index_page)
app.register_blueprint(sign_up_page)
app.register_blueprint(login_page)
app.register_blueprint(user_page)
app.register_blueprint(admin_page)
app.register_blueprint(errorhandler)

login_manager.init_app(app)

if __name__ == "__main__":
    app.run()
