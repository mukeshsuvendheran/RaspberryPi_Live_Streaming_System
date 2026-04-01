import sys
import os
import importlib
import pkgutil

sys.path.insert(0, "/home/sibidharan/iotweb")
os.chdir("/home/sibidharan/iotweb")

from flask import Flask
from flask import Flask, redirect, url_for, request, render_template, session
import os
import math
import base64
from src import get_config
from src.User import User



basename = get_config("basename")
application = app = Flask(__name__, static_folder='assets', static_url_path=basename)
app.secret_key = get_config("secret_key")

def register_blueprints(app, package_name, package_path):
    for _, module_name, _ in pkgutil.iter_modules([package_path]):
        if not module_name.startswith('_'):
            full_module_name = f'{package_name}.{module_name}'
            module = importlib.import_module(full_module_name)
            if hasattr(module, 'bp'):
                app.register_blueprint(module.bp)

@app.route(basename+"/dashboard")
def dashboard():
   return render_template('dashboard.html', session=session)

@app.route(basename+"/auth", methods=['POST'])
def authenticate():
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      return {
         "message": "Already Authenticated",
         "authenticated": True
      }, 202
   else:
      if 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']
         try:
            User.login(username, password)
            session['authenticated'] = True
            # return {
            #    "message": "Successfully Authenticated",
            #    "authenticated": True
            # }, 200
            return redirect(url_for('dashboard'))
         except Exception as e:
            return {
               "message": str(e),
               "authenticated": False
            }, 401
      else:
         return {
            "message": "Not enough parameters",
            "authenticated": False
         }, 400

@app.route(basename+"/deauth")
def deauth():
   if session.get('authenticated'): #TODO: Need more validattion like login expiry
      #Remove / invalidate session from database
      session['authenticated'] = False
      # return {
      #    "message": "Successfully Deauthed",
      #    "authenticated": False
      # }, 200
      return redirect(url_for('dashboard'))

register_blueprints(app, 'blueprints', 'blueprints')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=7000, debug=True)