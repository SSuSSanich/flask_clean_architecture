from flask import Blueprint, render_template, abort, request, redirect
from flask_login import LoginManager, login_user

from UserLogin import UserLogin
from config import ANONYMOUS_ID
from configuration.main_configuration import user_logger, logger
from src.dto.LoginInformation import LoginInformation

from src.exception.UserExistenceError import UserExistenceError
from src.exception.ValidationError import ValidationError

login_page = Blueprint('login_page', __name__,
                       template_folder='templates')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):  # gains id from saved in browser session cookies
    return UserLogin(user_id)


@login_manager.unauthorized_handler
def unauthorized_error():
    return render_template('unauthorized_error.html')


@login_page.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        is_remember = bool(request.form.get('remember_me'))

        login_info = LoginInformation(
            email,
            password,
        )

        output_user_credentials = None
        try:
            output_user_credentials = user_logger.login(login_info)
        except ValidationError as error:
            logger.save_log(request.remote_addr, ANONYMOUS_ID, str(error))
            abort(401, description="The incorrect username or password")
        except UserExistenceError as error:
            logger.save_log(request.remote_addr, ANONYMOUS_ID, str(error))
            abort(401, description=error)

        session_save = UserLogin(output_user_credentials.user_id)
        if is_remember:
            login_user(session_save)
        else:
            login_user(session_save)

        logger.save_log(request.remote_addr, session_save.get_id(), "Log In")

        return redirect("/main-page", 301)
    return render_template('login.html')