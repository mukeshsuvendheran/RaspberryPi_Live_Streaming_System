from flask import Flask, jsonify
from flask import redirect, url_for
import os

app = Flask(__name__)
basename = '/iotcloud'
@app.route("/")
def home():
    return "Flask is running successfully!" 

@app.route(basename + "/whoami")
def whoami():
    return os.popen("whoami").read().strip()   

#cpuinfo with error handling for admin user
#here admin user is not allowed to access cpuinfo
@app.route(basename + "/cpuinfo")
def cpuinfo():
    if isadmin() == 'User is admin':
        return redirect(url_for('error_page', error_code=1000))
    else:
        info = os.popen("cat /proc/cpuinfo").read().strip()
        return f"<pre>{info}</pre>"

@app.route(basename + "/error/<int:error_code>")
def error_page(error_code):
    if error_code == 1000:
        return "Error 1000: Admin users are not allowed to access CPU info.", 1000
    else:
        return " Other Unknown error."

#check admin user function
@app.route(basename + "/isadmin")
def isadmin():
    if whoami() == 'root':
        return "User is admin"
    else:
        return "User is not admin"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
