import speech_recognition as sr
import pyttsx3

# def SpeakText(command):
     
#     # Initialize the engine
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()

# def authenticate_user():
#     # Obtain audio from the user
#     mic = sr.Microphone(1)
#     r = sr.Recognizer()
#     with mic as source:
#         print("Say something to authenticate yourself")
#         r.adjust_for_ambient_noise(source, duration=0.2)
#         audio = r.listen(source)
#         user_input = r.recognize_google(audio,language='th')
#         print("You said: " + user_input)
        
    #Use speech recognition to convert audio to text
    # try:
    #     user_input = r.recognize_google(audio)
        
    #     # Authenticate user based on voice characteristics
    #     # Replace this with your own authentication logic
    #     if user_input == "Hello":
    #         print("Authentication successful")
    #     else:
    #         print("Authentication failed")
            
    # except sr.UnknownValueError:
    #     print("Could not understand audio")
    # except sr.RequestError as e:
    #     print("Could not request results from Google Speech Recognition service; {0}".format(e))

r = sr.Recognizer()
 
# Function to convert text to
# speech
def authenticate_user(command):
     
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
     
     
# Loop infinitely for user to
# speak
 
while(1):   
     
    # Exception handling to handle
    # exceptions at the runtime
    try:
         
        # use the microphone as source for input.
        with sr.Microphone() as source2:
             
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source2)
             
            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
 
            print("Did you say ",MyText)
            authenticate_user(MyText)

        if MyText == "hello":
            print("Authentication successful")
        else:
            print("Authentication failed")
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")


# authenticate_user()
