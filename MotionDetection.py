import imutils
import cv2
import numpy as np
import os
import time

import BinarySilhouette

motion_detected = False
cap = None

STD_DIMENSIONS =  {
   "480p": (640, 480),
   "720p": (1280, 720),
   "1080p": (1920, 1080),
   "4k": (3840, 2160),
}

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

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
   width, height = STD_DIMENSIONS["480p"]
   if res in STD_DIMENSIONS:
       width,height = STD_DIMENSIONS[res]
   ## change the current caputre device
   ## to the resulting resolution
   change_res(cap, width, height)
   return width, height

def change_res(cap, width, height):
   cap.set(3, width)
   cap.set(4, height)


def motion():
    global cap
    id = -1
    motion_detected=False

    Frame = 10
    MIN_MOVEMENT_SIZE = 7000
    MOVEMENT_DETECTED_TIME_HOLD = 100
    cap = cv2.VideoCapture(0)
    first_frame = None
    next_frame = None

    delay_counter = 0
    movement_persistent_counter = 0

    while True:
        transient_movement_flag = False
        ret, frame = cap.read()
        text = "No motion"
        if not ret:
            cap = cv2.VideoCapture(0)
            print("ERROR")
            continue
        frame = imutils.resize(frame, width=750)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        if first_frame is None: first_frame = gray

        delay_counter += 1
        if delay_counter > Frame:
            delay_counter = 0
            first_frame = next_frame
        next_frame = gray
        frame_delta = cv2.absdiff(first_frame, next_frame)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            if cv2.contourArea(c) > MIN_MOVEMENT_SIZE:
                transient_movement_flag = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if transient_movement_flag == True:
            movement_persistent_flag = True
            movement_persistent_counter = MOVEMENT_DETECTED_TIME_HOLD
        if movement_persistent_counter > 0:
            text = "Movement Detected " + str(movement_persistent_counter)
            movement_persistent_counter -= 1
            id = record()
            if id > 10000000:
                cap.release()
                return id

        else:
            text = "No Movement Detected"
        #frame_delta = cv2.cvtColor(frame_delta, cv2.COLOR_GRAY2BGR)
        #cv2.imshow("frame", np.hstack((frame_delta, frame)))
        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            break
    cv2.waitKey(0)
    cap.release()
     
    #cv2.destroyAllWindows()
def record():
    global cap, res
    filename = 'video.avi'
    frames_per_second = 24.0
    res = '720p'
    
    out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))
    timeout = time.time() + 4
    while True:
        ret, frame = cap.read()
        out.write(frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or time.time() > timeout:
            break
    out.release()
    return BinarySilhouette.preprocess(0)



    

#motion_detected = motion()
#print(motion_detected)
