from recogition.recordCommandVoice import recordVoice
from recogition.translateAudio import translateSpeechToText
from player.player import MusicIndexer, MusicPlayer
from os import path
import time

AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "../recorded/output.wav")
AUDIO_FOLDER = path.join(path.dirname(path.realpath(__file__)), "../worker/musics")
PREMIERE_CONFIGURATION = path.join(path.dirname(path.realpath(__file__)), "../worker/emcv_responses/premiere-connexion.wav")
PLAYLIST = path.join(path.dirname(path.realpath(__file__)), "../worker/emcv_responses/lire-playlist.wav")
PAS_DE_CONNEXION = path.join(path.dirname(path.realpath(__file__)), "../worker/emcv_responses/pas-de-connexion-internet.wav")
Indexer = MusicIndexer(AUDIO_FOLDER)
player = MusicPlayer(Indexer)

print("\n\n\n")
print(AUDIO_FOLDER)
print("\n\n\n")

RECORD_SECONDS = 4

def first_configuration():
    #ask to hellp user
    time.sleep(5)
    player.play_song(PREMIERE_CONFIGURATION)
    time.sleep(8)
    recordVoice(AUDIO_FILE, RECORD_SECONDS)
    resp = translateSpeechToText(AUDIO_FILE)
    if not "oui" in resp:
        return {
            "status": "failed"
        }
    #ask tthe user name
    username = ''
    while not username:
        player.play_song(PLAYLIST)
        recordVoice(AUDIO_FILE, RECORD_SECONDS)
        resp = translateSpeechToText(AUDIO_FILE)
        print("end recording")
        if resp:
            yes = input("votre nom est il {}?".format(resp))
            if yes == "yes":
                username = resp
            else:
               yes = input("continuer? ")
               if not yes == "yes":
                   break  
        else:
            player.play_song(PAS_DE_CONNEXION)
            
            
    
    