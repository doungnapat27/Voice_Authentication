import json
from flask import Flask, redirect, request, render_template, flash, url_for
from markupsafe import escape
import os

import scipy.io.wavfile as wav
import numpy as np
import sounddevice as sd
from python_speech_features import mfcc

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# route to the index page and the register page
@app.route("/")
def register():
    return render_template('register.html')


@app.route("/login")
def login():
    return render_template('login.html')

# use for register page


@app.route("/saveRecord", methods=['POST'])
def save_record(filename):
    print('Recording audio...')
    fs = 44100  # sampling frequency
    recording = sd.rec(int(fs * 5), samplerate=fs, channels=1)
    sd.wait()  # wait until recording is finished
    wav.write(f"data/audio/{filename}.wav", fs, recording)
    print(f"Saved audio to data/audio/{filename}.wav")


@app.route("/register", methods=['POST'])
def voice_register():
    if request.method == 'POST':

        username = request.form['username']
        save_record(username)
        # Save the data to a JSON file
        data = {
            "username": username,
            "filename": username+".wav"
        }
        json_file = 'data/user-data.json'

    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            json_data = json.load(f)
    else:
        json_data = []
    json_data.append(data)
    with open(json_file, 'w') as f:
        json.dump(json_data, f)

    return redirect(url_for('login'))


@app.route("/success")
def success():
    return render_template('success.html')


@app.route("/fail")
def fail():
    return render_template('fail.html')


@app.route("/record", methods=['POST'])
def record_audio(filename):
    print('[#] --- recording...')
    fs = 44100  # sampling frequency
    duration = 5  # duration of recording in seconds
    recording = sd.rec(int(fs * duration), samplerate=fs, channels=1)
    sd.wait()  # wait until recording is finished
    wav.write(filename, fs, recording)


def extract_features(filename):
    print('[#] --- extracting...')
    # load the audio file
    fs, audio = wav.read("data/audio/"+filename)

    # convert to mono if stereo
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # extract the Mel-frequency cepstral coefficients (MFCCs)
    mfcc_features = mfcc(audio, samplerate=fs, winlen=0.025,
                         winstep=0.01, numcep=13, nfilt=26, nfft=2048, preemph=0.97)

    # calculate the mean of each coefficient
    mean_features = np.mean(mfcc_features, axis=0)

    return mean_features


def authenticate_user(username):
    # record user's voice
    print("Please say the passphrase...")
    record_audio("user.wav")

    # extract features from recorded voice
    user_features = extract_features("user.wav")

    # load voice from the database of the specicified user
    json_file = 'data/user-data.json'

    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        data = []

    for user_data in data:
        print(data)
        if user_data['username'] == username:
            file = user_data['filename']

    # reference_features = extract_features(file)
    reference_features = extract_features(file)

    # calculate the similarity score between user and reference features
    from scipy.spatial.distance import cosine
    similarity_score = 1 - cosine(user_features, reference_features)

    # determine if user is authenticated or not
    if similarity_score >= 0.7:
        print("[x] --- User authenticated!...")
        return True
    else:
        print("[x] --- Access denied!...")
        return False


@app.route('/login', methods=['POST'])
def auth_login():
    username = request.form['username']
    if authenticate_user(username) == True:
        return render_template('success.html')
    return render_template('fail.html')


if __name__ == '__main__':
    app.run(debug=True)
