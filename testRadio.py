import vlc
import time


def playRadioFromSite(url):
    #url = "http://stream.revma.ihrhls.com/zc545"  # ed sheeran iheartradio station

    #url2 = "https://stream.revma.ihrhls.com/zc2341"  # lumineers iheartradio station

    player = vlc.MediaPlayer(url)

    player.play()
    while True:
        pass

    return null


def playRadioFromFile(fileName):

    fileName = "file_example_MP3_700KB.mp3"

    player = vlc.MediaPlayer(fileName)

    player.play()
    while True:
        pass

    return null

