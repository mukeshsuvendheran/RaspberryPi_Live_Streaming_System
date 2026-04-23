from flask import Flask,jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask is running"

@app.route("/whoami")
def whoami():
    return os.popen("whoami").read().strip() #strip used to remove extra newline

@app.route("/cpuinfo")
def cpuinfo():
    return os.popen("cat /proc/cpuinfo").read().strip()

@app.route("/hello/1/2")
def status():
    data = {
        "device": "Raspberry Pi",
        "service": "Flask API",
        "status": "OK"
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

