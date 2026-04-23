
from flask import Flask
from flask import redirect, url_for,request
import os

app = Flask(__name__)
basename = '/iotcloud'
@app.route("/")
def home():
    return "Flask is running successfully!" 

#dynamic routing
import math
@app.route(basename + "/paw/<int:a>/<int:b>")
def paw(a,b):  
    return f" The product of {a} and {b} is: {math.pow(a,b)}"

#square root
@app.route(basename + "/math/square", methods=['POST'])
def square():
    num = request.form.get('num')

    if num is None:
        return "num parameter is missing", 400

    return str(math.sqrt(float(num)))




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)