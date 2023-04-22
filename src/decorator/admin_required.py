from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(view):
    admin_id = 1

    @wraps(view)
    def decorated_view():
        if current_user.get_id() and int(current_user.get_id()) == admin_id:
            return view()
        else:
            abort(403, description="This page is only accessible to admin")
    return decorated_view
