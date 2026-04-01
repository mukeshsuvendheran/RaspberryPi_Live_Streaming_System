from flask import Flask, jsonify
import os

app = Flask(__name__)
basename = '/iotcloud'

@app.route("/")
def home():
    return "Flask is running successfully!"

@app.route(basename + "/whoami")
def whoami():
    return os.popen("whoami").read().strip()
    
@app.route(basename + "/cpuinfo")
def cpuinfo():
    info = os.popen("cat /proc/cpuinfo").read().strip()
    return f"<pre>{info}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)