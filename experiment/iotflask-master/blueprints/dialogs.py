from flask import Blueprint, render_template, redirect, url_for, request, session
from src.User import User
from src.Session import Session
from src.Group import Group
bp = Blueprint("api-dialogs", __name__, url_prefix="/api/dialogs/")

@bp.route('/api_keys')
def api_keys():
    groups = Group.get_groups()
    return render_template('dialogs/api_keys.html', session=session, groups=groups)