import vlc
import time

url = "http://stream.revma.ihrhls.com/zc281"

fileName = 'C:\\Downloads\file_example_MP3_700KB.mp3'

instance=vlc.Instance()
player = vlc.MediaPlayer(url)
player.play()
time.sleep(10)
