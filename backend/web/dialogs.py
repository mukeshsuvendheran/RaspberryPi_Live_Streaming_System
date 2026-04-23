from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config
from services.device_api_services import API
from services.group_services import Group

dialogs_bp = Blueprint("api-dialogs", __name__, url_prefix="/api/dialogs")

@dialogs_bp.route('/api_keys_dialog')
def api_keys_dialog():
    groups = Group.get_groups()
    return render_template('dialogs/api_keys_dialog.html', session=session, groups=groups)