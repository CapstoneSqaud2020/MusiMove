import numpy as np
import os
import cv2
import BinarySilhouette

import threading
from PIL import ImageTk, Image
import tkinter as tk
#import BinarySilhouette 


filename = 'video.avi'
frames_per_second = 24.0
res = '720p'

# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
   cap.set(3, width)
   cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
   "480p": (640, 480),
   "720p": (1280, 720),
   "1080p": (1920, 1080),
   "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
   width, height = STD_DIMENSIONS["480p"]
   if res in STD_DIMENSIONS:
       width,height = STD_DIMENSIONS[res]
   ## change the current caputre device
   ## to the resulting resolution
   change_res(cap, width, height)
   return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
   'avi': cv2.VideoWriter_fourcc(*'XVID'),
   #'mp4': cv2.VideoWriter_fourcc(*'H264'),
   'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
   filename, ext = os.path.splitext(filename)
   if ext in VIDEO_TYPE:
     return  VIDEO_TYPE[ext]
   return VIDEO_TYPE['avi']



#out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

def startVideoProc(self):
    self.stopEvent = False
    self.cap = cv2.VideoCapture(0)
    self.out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(self.cap, res))
    startVideo(self)


def startVideo(self):
    #out.write(frame)
    try:
        if not self.stopEvent:
        
            _, self.frame = self.cap.read()
            frame1 = cv2.flip(self.frame, 1)
            cv2image = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
        
            if self.panel is None:
                self.panel = tk.Label(self.root, bg="#80c1ff")
                self.panel.place(relwidth = .6, relheight = .6,relx = .2, rely = .2)
                self.panel.image = imgtk
            else:
                self.panel.configure(image=imgtk)
                self.panel.image = imgtk
            
            self.panel.after(10, lambda : startVideo(self))

    except RuntimeError:
        print("[INFO] caught a RuntimeError")
  
def stopVideoProc(self):
        self.stopEvent = True
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()
        t = threading.Thread(target = BinarySilhouette.preprocess, args = (self.user_id,))
        t.start()

def saveVideo(self):
    if not self.stopEvent:
         self.out.write(self.frame)
         self.panel.after(10, lambda : saveVideo(self))


#cap.release()
#out.release()
#cv2.destroyAllWindows()
