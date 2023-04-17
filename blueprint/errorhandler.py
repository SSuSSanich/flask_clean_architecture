from flask import Blueprint, render_template

errorhandler = Blueprint('errorhandler_page', __name__,
                         template_folder='templates')


@errorhandler.app_errorhandler(400)
def bad_request_error(error):
    return render_template('sign-up.html', error_message=error.description)


@errorhandler.app_errorhandler(401)
def unauthorized_error(error):
    return render_template('login.html', error_message=error.description)


@errorhandler.app_errorhandler(403)
def forbidden_error(error):
    return render_template('forbidden.html', error_message="Forbidden")