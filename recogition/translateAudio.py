#!/usr/bin/env python3

import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
#from os import path
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "english.wav")
#AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "recorded/output.wav")
# AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "chinese.flac")
# use the audio file as the audio source

def translateSpeechToText(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        translated_text = r.recognize_sphinx(audio, "fr-FR")
        return translated_text 
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
