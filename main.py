import json
from flask import Flask, redirect, request, render_template, flash, url_for
from markupsafe import escape
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
        username = request.form['username']

        if file and file.filename.endswith('.wav'):
            file.save(file.filename)
            flash('File uploaded successfully', 'success')
            # Save the data to a JSON file
            data = {
                "username": username,
                "filename": file.filename
            }
            json_file = 'user-data.json'
            if os.path.exists(json_file):
                with open(json_file, 'r') as f:
                    json_data = json.load(f)
            else:
                json_data = []
            json_data.append(data)
            with open('data/'+json_file, 'w') as f:
                json.dump(json_data, f)
        else:
            flash('Please upload a WAV file', 'danger')
    return redirect(url_for('register'))

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/fail")
def fail():
    return render_template('fail.html')


# route to the login page
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         # still waiting form the model from tan
#         user = request.form['file']
#         return render_template('success', name=user)


if __name__ == '__main__':
    app.run(debug=True)
