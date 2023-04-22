from flask import Flask
from flask import request
from markupsafe import escape
from flask import render_template,flash
import os


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# route to the index page and the register page
@app.route("/")
def register():
    return render_template('register.html')

@app.route("/uploadFile", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.wav'):
            file.save(file.filename)
            flash('File uploaded successfully', 'success')
        else:
            flash('Please upload a WAV file', 'danger')
    return render_template('register.html')



# route to the login page
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         # still waiting form the model from tan
#         user = request.form['file']
#         return render_template('success', name=user)


if __name__ == '__main__':
    app.run(debug=True)
