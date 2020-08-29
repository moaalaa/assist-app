import os
import random
import time
import webbrowser
from datetime import datetime

import playsound
import speech_recognition as sr
from gtts import gTTS

# Define our recognizer
r = sr.Recognizer()

# Define our record audio function
def record_audio(ask_question = False):
    # Listen to microphone source
    with sr.Microphone() as source:
        # Ask Question
        if ask_question:
            self_speak(ask_question)

        # Listen to source and get audio
        try:
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            self_speak("No Speaking for long time")
            
        voice_data = ''
        
        try:
            # Recognize audio with google and get voice data
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            self_speak("Sorry, i Didn't Understand!")
        except sr.RequestError:
            self_speak("I'm offline, Please check your internet connection")

        return voice_data


def response(voice_data):
    if 'what is your name' in voice_data:
        self_speak('My name is Assist')

    elif 'what is the time' in voice_data or 'what time is it' in voice_data:
        self_speak('Time is: ' + datetime.now().strftime("%H:%M:%S %p"))

    elif 'search' in voice_data or 'i want to search' in voice_data:
        search = record_audio("What do you want to search for ?")
        url = "https://google.com/search?q=" + search
        webbrowser.get().open(url)
        self_speak("I found this results for " + search)
    
    elif 'find location' in voice_data or 'find a location' in voice_data:
        location = record_audio("What location do you wants ?")
        url = "https://google.com/maps/place/" + location + "/&amp;"
        webbrowser.get().open(url)
        self_speak("I found location for " + location)

    elif 'exit' in voice_data or 'abort' in voice_data:
        self_speak("Ok, Goodby")
        exit()
    
    else:
        self_speak("Sorry, i Didn't Understand command " + voice_data)


def self_speak(audio_string):
    # Generate text to Speech data
    text_to_speech = gTTS(text=audio_string, lang="en")
    
    # Create A Random file Postfix
    random_file_postfix = random.randint(1, 100)
    
    # create speaking audio file
    audio_file = 'speak-' + str(random_file_postfix) + '.mp3'
    
    # save generated text to speech to created audio file
    text_to_speech.save(audio_file)

    # Play sound file
    playsound.playsound(audio_file)

    # Print audio string as well
    print(audio_string)

    # Remove created audio file
    os.remove(audio_file)
 
time.sleep(1)

self_speak("What is in your mind today ?")

while True:
    voice_data = record_audio()
    response(voice_data)
