import pygame.mixer as mixer
import os
import pathlib



class MusicIndexer:
    def __init__(self, dir_name):
        self.start(dir_name)
        
    def start(self, dir_name):
        self.root_dir = dir_name
        self.all_music = []
        self.musics_extensions = [".mp3", ".wav", ".m4a"]
        self.load(self.root_dir)
        self.state = {
            "playing": False,
            "current": None,
            "last": None,
        }
        self.state["last"] = len(self.all_music) - 1
    def load(self, dirname):
        if len(self.all_music) <= 300:
            for sChild in os.listdir(dirname):                
                sChildPath = os.path.join(dirname, sChild)
                if os.path.isdir(sChildPath):
                    self.load(sChildPath)
                else:
                    if pathlib.Path(sChildPath).suffix in self.musics_extensions:
                        self.all_music.append(sChildPath)
                        
    def getNext(self):
        if self.state["last"] != None and int(self.state["last"]) != 0:
            if self.state["current"] == None or self.state["current"] == self.state["last"]:
                return self.all_music[0]
            else:
                return self.all_music[int(self.state["current"])]
        return None
    
    def getPrev(self):
        if self.state["last"]:
            if self.state["current"] == 0:
                return self.all_music[int(self.state["last"])-1]
            else:
                return self.all_music[int(self.state["current"])]
        return None
    def getCurrent(self):
        if self.state["current"] != None and (int(self.state["current"]) >= 0 and int(self.state["current"]) < int(self.state["last"])):
            return self.all_music[int(self.state["current"])]
        else:
            return None
    
    def nextIndex(self):
        if self.state["current"]:
            if int(self.state["current"]) == int(self.state["last"]):
                self.state["current"] = 0
            else:
                self.state["current"] = int(self.state["current"]) + 1
                print("\n\n{}\n\n".format(int(self.state["current"])))
        
    def prevIndex(self):
        if int(self.state["current"]) == 0:
            self.state["current"] = int(self.state["last"])
        else:
            self.state["current"] -= 1
            
    def search(self, keyword):
        for elem in self.indexer.all_music:
            if keyword in elem.split("/")[len(elem.split("/") - 1)]:
                return self.indexer.all_music.index(elem)
        return ""
            
            

class MusicPlayer:
    def __init__(self, musicIndexer):
        self.indexer = musicIndexer
        if self.indexer.all_music:
            self.indexer.state["current"] = -1
            self.mixer = mixer
        # Initializing the mixer
        self.mixer.init()
        
        
    def play_song(self, song_name):
        self.mixer.music.load(song_name)
        self.mixer.music.play()
        self.indexer.state["playing"] = True
        return True
    def stop_song(self):
        self.mixer.music.stop()
        self.indexer.state["playing"] = False
    
    def pause_song(self):
        self.mixer.music.pause()
        self.indexer.state["playing"] = False
    def resume_song(self):
        self.mixer.music.unpause()
        self.indexer.state["playing"] = True
    def next_song(self):
        if self.indexer.all_music:
            if self.indexer.state["current"] >= self.indexer.state["last"]:
                self.indexer.state["current"] = -1
            else:
                self.indexer.state["current"] = self.indexer.state["current"] + 1
            self.indexer.nextIndex()
            song_name = self.indexer.getCurrent()
            if song_name:
                print(song_name)
                return self.play_song(song_name)
        return False
    def prev_song(self):
        if self.indexer.all_music:
            if self.indexer.state["current"] <= -0:
                self.indexer.state["current"] = int(self.indexer.state["last"]) - 1
            else:
                self.indexer.state["current"] = self.indexer.state["current"] - 1
            song_name = self.indexer.getCurrent()
            if song_name:
                return self.play_song(song_name)
        return False
    def check_if_finished(self):
        if not self.indexer.state["playing"] or self.mixer.music.get_busy():
            return True
        else:
            return False