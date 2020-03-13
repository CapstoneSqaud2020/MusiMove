import os
import cv2
import numpy as np
import scipy.signal
import lmfit
import itertools

#import pickle
import FeatrueExtractionforNewUsers
import shutil

def grouped(iterable, n):
    return zip(*[iter(iterable)]*n)

def func(params, t, y):
    phi = params['phi'].value
    offset = params['offset'].value
    omega = params['omega'].value
    amp = params['amp'].value
    return amp *np.sin(omega*( t + phi)) + offset - y 

 

def findGait(user_id):
    PATH =  "silhouettes"
    seq_num = 0
    gaits = []

    for x in os.walk(PATH):
        if (x[0] != PATH):

            n = 0
            sqrt1 = 0
            sqrt2 = 0
            frame =[]
            NAC = []
            imgs = []
            for i in  range(len(x[2])-1):
                img1 =cv2.imread(os.path.join(x[0], x[2][i]), cv2.IMREAD_GRAYSCALE)
                img2 =cv2.imread(os.path.join(x[0], x[2][i+1]),cv2.IMREAD_GRAYSCALE)
                n = cv2.sumElems(cv2.multiply(img1,img2))[0]
                sqrt1 = cv2.sumElems(cv2.multiply(img1,img1))[0]
                sqrt2 = cv2.sumElems(cv2.multiply(img2,img2))[0]
                C = n/(np.sqrt(sqrt1)*np.sqrt(sqrt2))
                frame.append(int(x[2][i][:-4]))
                NAC.append(C)

                imgs.append(img1)
                if i == len(x[2])-1:
                    imgs.append(img2)

            if(len(NAC)>2):    
                frame = np.array(frame)
                NAC = np.array(NAC)*10**-1
        
                params = lmfit.Parameters()
                params.add('offset', 2.0, min=0, max=10.0)
                params.add('omega', .2, min=0.1, max=1.0)
                params.add('amp', 2.5, min=0, max=10.0)
                params.add('phi', 1.0, min==0, max=10.0)
                opt = lmfit.minimize(func, params, args = (frame,NAC), method = 'differential_evolution') 

                fitted = NAC+opt.residual
                peaks = scipy.signal.find_peaks(fitted)
        
                if(len(peaks[0])>1 and len(frame)/len(peaks[0]) > 10):
                    for p1, p2 in grouped(peaks[0],2):
                        seq_num += 1
                        gaits.append({"usr_id":user_id, "seq_num":seq_num, "startFrame":frame[p1], "endFrame":frame[p2], "cycleImgs":imgs[p1:p2+1]})

                elif len(peaks[0])>1:
                    for p1, p2, p3 in grouped(peaks[0],3):
                        seq_num += 1
                        gaits.append({"usr_id":user_id, "seq_num":seq_num, "startFrame":frame[p1], "endFrame":frame[p2], "cycleImgs":imgs[p1:p2+1]})


    #shutil. rmtree(PATH) 
    return FeatrueExtractionforNewUsers.callModel(gaits)      


        


            
