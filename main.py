from flask import Flask
from flask import request
from markupsafe import escape
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('register.html')

@app.route('/login',methods = ['POST'])
def login():
   if request.method == 'POST':
      #still waiting form the model from tan
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   app.run(debug = True)