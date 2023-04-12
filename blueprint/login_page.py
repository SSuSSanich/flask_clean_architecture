from flask import Blueprint, render_template, abort

login_page = Blueprint('login_page', __name__,
                       template_folder='templates')


@login_page.route('/mega-login')
def show():
    return render_template(f'login.html')