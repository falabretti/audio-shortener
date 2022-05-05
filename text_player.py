import pyttsx3


def speak_text(text):
    out = pyttsx3.init()    
    out.say(text)
    out.runAndWait()
