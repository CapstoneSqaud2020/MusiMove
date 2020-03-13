import vlc
import time
import os
from mutagen.mp3 import MP3

player = None
is_paused = True

def setRadio(url):
    global player
    player= vlc.MediaPlayer(url)

def setPlaylist():
    global player
    musicFolder = "C:\\Users\\aishw\\Desktop\\Capstone Stuff\\mpSongs"
    songs = os.listdir(musicFolder)

    for x in range(len(songs)):
        song = MP3(musicFolder + "\\" + songs[x])
        songLength = song.info.length

        os.startfile(musicFolder + "\\" + songs[x])

        time.sleep(songLength)
        is_paused = False

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
