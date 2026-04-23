#blueprints/home.py
from flask import Blueprint, render_template, redirect, url_for, request, session
from utils import get_config, time_ago, mask
from services.device_api_services import API
from services.group_services import Group


dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/")

@dashboard_bp.route("/")
def index():
    return "I am home"

@dashboard_bp.route("/dashboard")
def dashboard():
   return render_template('dashboard.html', session=session)

@dashboard_bp.route("/api_keys")
def api_keys():
   groups = list(Group.get_groups())
   api_keys = API.get_all_keys(session)
   return render_template('api_keys.html', session=session, api_keys=api_keys, groups=groups, time_ago=time_ago, mask=mask)

@dashboard_bp.route("/api_keys/row")
def api_keys_row():
   api_key_hash = request.args.get('hash')
   api = API(api_key_hash)
   groups = Group.get_groups()
   return render_template('api_keys/row.html', key=api.collection._data, groups=groups, time_ago=time_ago, mask=mask)

@dashboard_bp.route("/api_keys/row/delete_dialog")
def api_keys_delete_dialog():
   api_key_hash = request.args.get('hash')
   api = API(api_key_hash)
   return render_template('dialogs/delete_api_key.html', key=api.collection._data, time_ago=time_ago, mask=mask)

@dashboard_bp.route("/api_keys/row/delete", methods=["POST"])
def api_keys_delete():
   api_key_hash = request.args.get('hash')
   api = API(api_key_hash)
   api.delete()
   return {
      'status': 'success'
   }, 200

@dashboard_bp.route("/api_keys/enable", methods=['POST'])
def enable_api_key():
   api_key_hash = request.form['id']
   api_key_status = request.form['status']
   print(bool(api_key_status))
   api = API(api_key_hash)
   api.collection.active = api_key_status == "true"
   return {
      'status': api.collection.active
   }, 200