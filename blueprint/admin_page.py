from typing import List

from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from configuration.main_configuration import logger
from src.decorator.admin_required import admin_required
from src.dto.ResponseLog import ResponseLog
from src.dto.SearchLogParameter import SearchLogParameter

admin_page = Blueprint('admin_page', __name__,
                       template_folder='templates')


@admin_page.route('/admin-panel', methods=["GET", "POST"])
@admin_required
def admin_panel_page():
    parameter = SearchLogParameter(" ", 1, " ")
    offset = 0
    response_log_list: List[ResponseLog] = logger.get_logs_by_parameters(offset, parameter)

    return render_template('admin_panel.html', log_list=response_log_list)


@admin_page.route('/admin-panel/load-more-posts')
@admin_required
def load_more_posts():
    page = request.args.get('page', 1, int)
    offset = int(page)

    parameter = SearchLogParameter(" ", 1, " ")
    response_log_list: List[ResponseLog] = logger.get_logs_by_parameters(offset, parameter)

    return jsonify(logs=list(map(lambda log: log.get_json(), response_log_list)))