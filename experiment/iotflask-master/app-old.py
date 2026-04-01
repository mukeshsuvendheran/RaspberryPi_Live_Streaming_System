from flask import Flask
from flask import Flask, redirect, url_for, request, render_template
import os
import math

app = Flask(__name__, template_folder="templates-old")
basename = '/iotcloud'


@app.route(basename+"/hello_world")
def hello_world():
   d = {
      "username": whoami().strip(),
      "env": "labs",
      "avatar": "https://sibidharan.me/wp-content/uploads/2020/06/Logo-round.png"
   }
   return render_template('helloworld.html', data=d)
   
@app.route(basename+"/dashboard")
def dashboard():
   return render_template('dashboard.html', data={
      "title": "IoT Dashboard"
   })

@app.route(basename+'/')
def hello():
   return "<h1/>Welcome to Selfmade Ninja Academy</h1>"

@app.route(basename+'/whoami')
def whoami():
   return os.popen('whoami').read()

@app.route(basename+'/cpuinfo')
def cpuinfo():
   if isadmin() == "yes":
      return redirect(url_for('error', errorcode=1000))
   else:
      return "<pre>"+os.popen('cat /proc/cpuinfo').read()+"</pre>"
      
@app.route(basename+"/error/<int:errorcode>")
def error(errorcode):
   if errorcode == 1000:
      return "This app is running as root user, which is dangerous";
   elif errorcode == 1001:
      return "Some other error"
   else:
      return "Unknown error"

@app.route(basename+'/echo')
def echo_help():
   return "Please use as /echo/{some string}"

@app.route(basename+'/echo/<string>')
def echo(string):
   return "You said: {}".format(string)

@app.route(basename+"/isadmin")
def isadmin():
   if whoami().strip() == "root":
      return "yes"
   else:
      return "No, you are: "+whoami()
   
#dynamic routing
@app.route(basename+'/pow/<int:a>/<int:b>')
def power(a, b):
   try:
      return "Pow of {}, {}: {}".format(a, b, math.pow(a,b))
   except:
      return "This is too much... "
   

@app.route(basename+'/path/<path:a>')
def path_test(a):
      return("<code>"+a+"</code>")


@app.route(basename+"/math/sqrt", methods=['GET', 'POST'])
def math_sqrt():
   return {
      "result": str(math.sqrt(int(request.form['num'])))
   }





if __name__ == '__main__':
   app.run(host='0.0.0.0', port=7000, debug=True)