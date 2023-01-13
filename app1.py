from flask import Flask
from recogition.recordCommandVoice import recordVoice
from recogition.translateAudio import translateSpeechToText
from recogition.textToSpeech import textToSpeech
from command.parser import extract_command
from os import path
from player.player import MusicIndexer, MusicPlayer
from configs.first import first_configuration
import time


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "recorded/output.wav")
AUDIO_FILE_OUTPUT = path.join(path.dirname(path.realpath(__file__)), "recorded/input.wav")
AUDIO_FOLDER = path.join(path.dirname(path.realpath(__file__)), "worker/musics")
ERROR_NOTFILE_FOUND = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/musique_introuvable.wav")
ERREUR_REPETER = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/erreur-ecoute-repeter.wav")
BONJOUR_MADAME = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/bonjour-madame.wav")
BONJOUR_MONSIEUR = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/bonjour-monsieur.wav")
BONSOIR_MADAME = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/bonsoir-madame.wav")
BONSOIR_MONSIEUR = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/bonsoir-monsieur.wav")
SOURDINE = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/d'accord-mise-en-sourdine.wav")
ECHEC = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/echec.wav")
EXTINCTION = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/exteinction.wav")
INTRODUCTION = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/intro.wav")
PLAYLIST = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/lire-playlist.wav")
OK = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/ok.wav")
OPTION_INDISPONIBLE = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/option-indisponible.wav")
PAS_DE_CONNEXION = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/pas-de-connexion-internet.wav")
PLAYLIST_CREE = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/playlist-cree.wav")
PLAYLIST_INTROUVABLE = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/playlist-introuvable-creer.wav")
PREMIERE_CONFIGURATION = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/premiere-connexion.wav")
VERIFICATION_PERFORMANCE = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/verification-performances.wav")


RECORD_SECONDS = 4

Indexer = MusicIndexer(AUDIO_FOLDER)
player = MusicPlayer(Indexer)

app = Flask(__name__)

@app.route("/")
def configure_first():
    pass
    
@app.route("/musicplayer/play")
def play():
    if not player.next_song():
        player.play_song(ERROR_NOTFILE_FOUND)
        return {
            "status": "success",
        }
    return {
        "status": "failed",
    }
@app.route('/musicplayer/play/next')
def play_next():
    return 'Hello, World'

@app.route('/musicplayer/play/prev')
def play_prev():
    return 'Hello, World'

@app.route('/commandreader/record')
def reccordAndProcess():
    recordVoice(AUDIO_FILE, RECORD_SECONDS)
    speech_text = translateSpeechToText(AUDIO_FILE)
    extract_command(speech_text, player)