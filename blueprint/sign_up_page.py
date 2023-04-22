from flask import Blueprint, render_template, abort, request

from config import ANONYMOUS_ID
from configuration.main_configuration import user_registrar, logger
from src.dto.InputUserCredentials import InputUserCredentials
from src.exception.EmailExistenceError import EmailExistenceError
from src.exception.PasswordMismatch import PasswordMismatchError
from src.exception.ValidationError import ValidationError


sign_up_page = Blueprint('sign_up_page', __name__,
                         template_folder='templates')


@sign_up_page.route('/sign-up', methods=["GET", "POST"])
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
            logger.save_log(request.remote_addr, ANONYMOUS_ID, str(error))
            abort(400, description=error)
        except EmailExistenceError as error:
            logger.save_log(request.remote_addr, ANONYMOUS_ID, str(error))
            abort(400, description=error)
        except PasswordMismatchError as error:
            logger.save_log(request.remote_addr, ANONYMOUS_ID, str(error))
            abort(400, description=error)

        logger.save_log(request.remote_addr,
                        ANONYMOUS_ID,
                        f"The user is registered as {user_data.name} with email: {user_data.email}")
        return render_template('login.html')

    return render_template('sign-up.html')