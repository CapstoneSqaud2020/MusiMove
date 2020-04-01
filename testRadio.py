import vlc
import time

import os
from mutagen.mp3 import MP3

player = None
is_paused = True

def setRadio(url):
    global player 
    player= vlc.MediaPlayer(url)

def playPlaylist():
    global player
    musicFolder = "Music"
    songs = os.listdir(musicFolder)

    is_paused = False
    while not is_paused:
        for s in songs:
            stop()
            song = MP3(musicFolder + "\\" + s)
            songLength = song.info.length

            setRadio(musicFolder + "\\" + s)
            player.play()
            time.sleep(songLength)
            
    is_paused = True

def play():
    global player, is_paused 
    if not(player is None) and is_paused:
        player.play()
        is_paused = False

def pause():

    global player, is_paused 
    if not (player is None and is_paused):
        player.pause()
        is_paused = True

def stop():
    global player, is_paused
    if not(player is None):
        player.stop()
    is_paused = True

def isPaused():
    if not is_paused:
        is_paused = not player.is_playing()
    return is_paused

