import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

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
    fs, audio = wav.read(filename)
    
    # convert to mono if stereo
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    
    # extract the Mel-frequency cepstral coefficients (MFCCs)
    from python_speech_features import mfcc
    mfcc_features = mfcc(audio, samplerate=fs, winlen=0.025, winstep=0.01, numcep=13, nfilt=26, nfft=2048, preemph=0.97)
    
    # calculate the mean of each coefficient
    mean_features = np.mean(mfcc_features, axis=0)
    
    return mean_features

def authenticate_user():
    # record user's voice
    print("Please say the passphrase...")
    record_audio("user.wav")
    
    # extract features from recorded voice
    user_features = extract_features("user.wav")
    
    # load reference features (previously extracted from authorized user's voice)
    reference_features = np.load("reference_features.npy")
    
    # calculate the similarity score between user and reference features
    from scipy.spatial.distance import cosine
    similarity_score = 1 - cosine(user_features, reference_features)
    
    # determine if user is authenticated or not
    if similarity_score >= 0.9:
        print("[x] --- User authenticated!...")
    else:
        print("[x] --- Access denied!...")


# def main():
#     record_audio("voice-dech.m4a")
#     reference_features = extract_features("voice-dech.m4a")
#     np.save("reference_features.npy", reference_features)
#     authenticate_user()

# if __name__ == '__main__':
#     main()