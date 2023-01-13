import speech_recognition as sr

def translateSpeechToText(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    try:
        translated_text = r.recognize_google(audio, "fr-FR")
        return translated_text 
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
