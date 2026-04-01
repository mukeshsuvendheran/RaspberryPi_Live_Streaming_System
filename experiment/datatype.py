from flask import Flask, jsonify

app = Flask(__name__)
basename = '/iotcloud'

@app.route("/")
def home():
    return "Flask is running"
#data types
@app.route(basename + "/datatype")
def datatype():
    data = {
        "integer": 42,
        "float": 3.14,
        "string": "Hello, World!",
        "boolean": True,
        "list": [1, 2, 3, 4, 5],
        "dictionary": {"key1": "value1", "key2": "value2"},
        "null_value": None
    }
    return jsonify(data)

#echo function in string
@app.route(basename + "/echo")
def echo_help():
    message = "This is an echo message as /echo/{some string}."
    return message

@app.route(basename + "/echo/<string:message>")
def echo(message):  
  #  return "Hii this is " + message
  #  return "Hii this is {}".format(message)
     return f" Hii this is {message}"

#echo function in integer
@app.route(basename + "/echo/<int:number>")
def echo_number(number):  
    return f" You have entered number: {number}"

#paw function in integer
import math
@app.route(basename + "/paw/<int:a>/<int:b>")
def paw(a,b):  
    return f" The product of {a} and {b} is: {math.pow(a,b)}"

@app.route(basename + "/path/<path:a>")
def path(a):  
    return f" <code>{a}</code>" 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
