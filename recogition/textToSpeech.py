from gtts import gTTS
import os

def textToSpeech(textToTransform, inputPath):
    language = 'fr'
    myobj = gTTS(text=textToTransform, lang=language, slow=False)
    myobj.save(inputPath)
    os.system(inputPath)
    