import os
import shutil
import sklearn.preprocessing
import numpy as np 
import cv2 
import GaitIsolation


def preprocess(user_id):
    #gets video
    cap = cv2.VideoCapture('video.avi') 
    #cap = cv2.VideoCapture(r'C:\Users\JS-X360\Pictures\Original-20200129T082016Z-001\Original\N2_Trim.avi') 
    width  = cap.get(3)
    #filter to subtract bg
    fgbg = cv2.createBackgroundSubtractorKNN() 
    #set shadows to black
    fgbg.setShadowValue(0)
    PATH = "silhouettes"
    if not os.path.exists(PATH):
        os.makedirs(PATH)

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5))
    f = 0
    folder = os.path.join(PATH, f'{f:03}')
    img = 1
    current = 0
    prev = current

    while(1):
        #get frame from video
        ret, frame = cap.read()
    
        if frame is None:
            break
        #removes bg
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

        #thresh, fgmask = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
    
        con, h = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        con = sorted(con,key = cv2.contourArea, reverse = True) 

        #finds the person
        for c in con:
            x,y,w,h = cv2.boundingRect(c)
            i = int((2*x+w)/2)
            d = int(((88*h)/128)/2)
            #checks where they are
            if i> width/3 and i< 2*width/3:
                current = 1
                if current != prev :
                    #creates folder
                    folder = os.path.join(PATH, f'{f:03}')
                    f = f+1
                    if not os.path.exists(folder):
                        os.makedirs(folder)

                ROI = fgmask[y:y+h,i-d:i+d]
                ROI = cv2.resize(ROI,(88,128))
                ROI = cv2.normalize(ROI,  ROI, 0, 255, cv2.NORM_MINMAX)
            
                avg = cv2.sumElems(ROI)[0]/(225*88*128) 
                if(avg <= .6 and avg >= .15):
                    #saves the image
                    cv2.imwrite(folder + '\\' + f'{img:08}' + '.png',ROI)
                    img = img+1
           
            else:
                current = 0
                if os.path.exists(folder):
                    if not os.listdir(folder):
                        os.rmdir(folder)
            prev = current
            break

    cap.release() 
    cv2.destroyAllWindows() 
    os.remove('video.avi')

    return GaitIsolation.findGait(user_id)

