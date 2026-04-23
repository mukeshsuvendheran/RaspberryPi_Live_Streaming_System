# app.py
import sys
sys.path.append('/home/MUKESH/iotweb')

from flask import Flask, redirect, url_for, request, render_template, session
import os
from models.help import get_config
from web.dashboard import dashboard_bp
from routes.device.api_key_routes import device_bp
from services.device_api_services import API
from utils.file_handler import files_bp
from web.dialogs import dialogs_bp
from web.devices import devices_bp
from routes.auth.devices_auth import devices_auth_bp
from routes.auth.user_auth import userauth_bp
from models.motion import motion_bp


application = app = Flask(__name__, static_folder='assets', static_url_path="/")
app.secret_key = get_config("secret_key")

@app.before_request
def before_request_hook():
   if session.get('type') == 'web':
      return
   
   auth_header = request.headers.get('Authorization') 
   if auth_header:
      auth_token = auth_header.split(" ")[1]
      print(auth_token)
      try:
         api = API(auth_token)
         session['authenticated'] = api.is_valid()
         session['username'] = api.collection.username
         session['type'] = 'api'
         session['sessid'] = None
      except Exception as e:
         return "Unauthorized: "+str(e), 401
   else:
      session['authenticated'] = False
      if 'username' in session:
         del session['username']

#TODO: Automate importing blueprints from blueprints folder

app.register_blueprint(dashboard_bp)
app.register_blueprint(device_bp)
app.register_blueprint(files_bp)
app.register_blueprint(motion_bp)
app.register_blueprint(dialogs_bp)
app.register_blueprint(devices_bp)
app.register_blueprint(devices_auth_bp)
app.register_blueprint(userauth_bp)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)

