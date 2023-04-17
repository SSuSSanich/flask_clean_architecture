from flask import Blueprint, render_template
from flask_login import login_required

user_page = Blueprint('user_page', __name__,
                      template_folder='templates')


@user_page.route('/main-page')
@login_required
def user_main_page():
    return render_template('user_main_page.html')
