from os import path

OPTION_INDISPONIBLE = path.join(path.dirname(path.realpath(__file__)), "../worker/emcv_responses/option-indisponible.wav")

def extract_command(speech_text, player):
    if "shutdown" in speech_text:
        return {
            "action": "shutdown"
        }
    elif "stop" in speech_text:
        return {
            "action": "stop"
        }
    elif "play" in speech_text:
        if speech_text.strip().lower() == "play":
            player.next_song()
        else:
            try:
                music = player.indexer.search(speech_text.split("play")[1])
                if music:
                    player.play_song(music)
            except:
                player.play_song(OPTION_INDISPONIBLE)
        
    elif "pause" in speech_text:
        return {
            "action": "pause",
        }
    elif  "resume" in speech_text:
        return {
            "action": "resume",
        }
    elif  "next" in speech_text:
        return {
            "action": "next",
        }
    elif  "previous" in speech_text:
        return {
            "action": "previous",
        }
    elif  "name" in speech_text:
        return {
            "action": "name",
        }
    
    return speech_text
