import vlc
import time


player = None
is_paused = True

def setRadio(url):
    global player 
    player= vlc.MediaPlayer(url)

def setPlaylist():
    global player


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


