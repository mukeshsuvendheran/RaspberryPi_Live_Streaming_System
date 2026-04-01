# app.py
import sys
sys.path.append('/home/MUKESH/iotweb')

from flask import Flask, redirect, url_for, request, render_template, session
import os
from src import get_config
from src.user import User
from src.API import API
from blueprints import home, api, files, motion, dialogs, devices, devices_api

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

app.register_blueprint(home.bp)
app.register_blueprint(api.bp)
app.register_blueprint(files.bp)
app.register_blueprint(motion.bp)
app.register_blueprint(dialogs.bp)
app.register_blueprint(devices.bp)
app.register_blueprint(devices_api.bp)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)