from flask import Blueprint, render_template
from flask_login import current_user

from src.decorator.admin_required import admin_required

admin_page = Blueprint('admin_page', __name__,
                       template_folder='templates')


@admin_page.route('/admin-panel', methods=["GET", "POST"])
@admin_required
def admin_panel_page():
    return render_template('admin_panel.html', user_id=current_user.get_id())
