from flask import Flask, request, render_template, redirect, abort, Response
from markupsafe import escape
from flask_login import LoginManager, login_user, login_required
import sqlalchemy as postgres_db
from sqlalchemy import text

from blueprint.errorhandler import errorhandler
from blueprint.login_page import login_page

from src.database.FileDatabase import FileDatabase
from src.database.PGDatabase import PGDatabase
from src.database.IDatabaseGateway import IDatabaseGateway
from src.dto.InputUserCredentials import InputUserCredentials
from src.dto.LoginInformation import LoginInformation
from src.exception.EmailExistenceError import EmailExistenceError
from src.exception.PasswordMismatch import PasswordMismatchError
from src.exception.UserExistenceError import UserExistenceError
from src.exception.ValidationError import ValidationError
from src.usecase.HashLibPasswordHasher import HashLibPasswordHasher
from src.usecase.IPasswordHasher import IPasswordHasher
from src.usecase.IUserLogger import IUserLogger
from src.usecase.IUserRegistrar import IUserRegistrar
from src.usecase.IValidator import IValidator
from src.usecase.SimpleUserLogger import SimpleUserLogger
from src.usecase.SimpleUserRegistrar import SimpleUserRegistrar
from src.usecase.SimpleValidator import SimpleValidator

from UserLogin import UserLogin

from config import FLASK_SECRET_KEY, HASH_SECRET_KEY

app = Flask(__name__)
login_manager = LoginManager(app)
app.register_blueprint(login_page)
app.register_blueprint(errorhandler)

app.config['SECRET_KEY'] = FLASK_SECRET_KEY

database: IDatabaseGateway = PGDatabase()
validator: IValidator = SimpleValidator()
password_hasher: IPasswordHasher = HashLibPasswordHasher(HASH_SECRET_KEY)
user_registrar: IUserRegistrar = SimpleUserRegistrar(validator, database, password_hasher)
user_logger: IUserLogger = SimpleUserLogger(database, validator, password_hasher)


@login_manager.user_loader
def load_user(user_id):  # gains id from saved in browser session cookies
    return UserLogin(user_id)


@login_manager.unauthorized_handler
def unauthorized_error():
    return render_template('unauthorized_error.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/main-page')
@login_required
def user_main_page():
    return render_template('user_main_page.html')


@app.route('/sign-up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        retyped_password = request.form.get('retyped_password')
        email = request.form.get('email')

        user_data = InputUserCredentials(name, password, retyped_password, email)
        try:
            user_registrar.register(user_data)
        except ValidationError as error:
            app.logger.info(f"ValidationError: {error}")
            abort(400, description=error)
        except EmailExistenceError as error:
            app.logger.info(f"EmailExistenceError")
            abort(400, description=error)
        except PasswordMismatchError as error:
            app.logger.info("PasswordMismatchError")
            abort(400, description=error)

        return render_template('login.html')
    return render_template('sign-up.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        is_remember = bool(request.form.get('remember_me'))
        app.logger.info(f"remember_me: {is_remember}")

        login_info = LoginInformation(
            email,
            password,
        )

        output_user_credentials = None
        try:
            output_user_credentials = user_logger.login(login_info)
        except ValidationError as error:
            app.logger.info(f"ValidationError: {error}")
            abort(401, description="The incorrect username or password")
        except UserExistenceError as error:
            app.logger.info("UserExistenceError")
            abort(401, description=error)

        session_save = UserLogin(output_user_credentials.user_id)
        if is_remember:
            login_user(session_save)
        else:
            login_user(session_save)

        return redirect("/main-page", 301)
    return render_template('login.html')


if __name__ == "__main__":
    app.run()
