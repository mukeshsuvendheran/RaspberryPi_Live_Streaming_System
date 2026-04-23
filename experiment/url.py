from flask import Flask, jsonify
import os

app = Flask(__name__)
basename = '/iotcloud'

@app.route("/")
def home():
    return "Flask is running successfully!"

def whoami():
    return os.popen("whoami").read().strip()

def cpuinfo():
    info = os.popen("cat /proc/cpuinfo").read().strip()
    return f"<pre>{info}</pre>" # Wrap in <pre> for better formatting

app.add_url_rule(basename + '/whoami', 'whoami', whoami)
app.add_url_rule(basename + '/cpuinfo', 'cpuinfo', cpuinfo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
