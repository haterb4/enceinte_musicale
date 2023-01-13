from recogition.recordCommandVoice import recordVoice
from recogition.translateAudio import translateSpeechToText
from command.parser import extract_command
from os import path
from player.player import MusicIndexer, MusicPlayer


AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "recorded/output.wav")
AUDIO_FOLDER = path.join(path.dirname(path.realpath(__file__)), "worker/musics")
ERROR_NOTFILE_FOUND = path.join(path.dirname(path.realpath(__file__)), "worker/emcv_responses/erreur-ecoute-repeter.wav")
RECORD_SECONDS = 4



perform_action = False
Indexer = MusicIndexer(AUDIO_FOLDER)
player = MusicPlayer(Indexer)
while True:
    if perform_action:
        response = input("wich action: ")
        if response == 'p':
            if not player.next_song():
                player.play_song(ERROR_NOTFILE_FOUND)
        elif response == 'r':
            recordVoice(AUDIO_FILE, RECORD_SECONDS)
            speech_text = translateSpeechToText(AUDIO_FILE)
            command_word = extract_command(speech_text)
            if 'bonjour' not in command_word:
                player.play_song(ERROR_NOTFILE_FOUND)
                player.play_song(ERROR_NOTFILE_FOUND)
        elif response == 'n':
            if not player.next_song():
                player.play_song(ERROR_NOTFILE_FOUND)
        elif response == 'q':
            break
    new_action = input("new action? ")
    if new_action.lower() in ['non', 'n']:
        perform_action = False
    else:
        perform_action = True

exit(0)