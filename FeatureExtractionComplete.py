#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import final_cnn_load as fcl

def findGEI(preProcessedData):
    
    GEIs = []
    testDf = pd.DataFrame()
    testDf = pd.DataFrame.from_dict(preProcessedData, dtype = 'uint8')
    
    for d in preProcessedData:
        tempArr = np.asarray(d.get("cycleImgs"))
        GEIs.append(np.mean(tempArr, axis = 0))
        
    subIds = pd.DataFrame.to_numpy(testDf['usr_id'], dtype = 'int32')
    
    return GEIs, subIds


# In[2]:


from sklearn.model_selection import train_test_split

def getFeatures(preProcessedData):
    
    combinedGEIs, subIds = findGEI(preProcessedData)
    
    X_train, X_test, y_train, y_test = train_test_split(combinedGEIs, subIds, test_size=0.30, random_state=42, stratify = subIds)
    
    return X_train, X_test, y_train, y_test


# In[3]:


def shuffleFeatures(xTrain, yTrain, xTest, yTest):
    
    np.random.shuffle(xTrain)
    np.random.shuffle(yTrain)
    np.random.shuffle(xTest)
    np.random.shuffle(yTest)
    
    return xTrain, yTrain, xTest, yTest


# In[4]:


import os
import pickle

def loadFile(file):
    data = []
    with open(file, 'rb') as f:
                 data = pickle.load(f)        
            
    return data  


# In[5]:


def saveFile(fileToSave, file):
    with open(file, 'wb') as f:
        pickle.dump(fileToSave, f)
    
    return


# In[21]:


def addNewClass(preProcessedData):
    xTrainNew, xTestNew, yTrainNew, yTestNew = getFeatures(preProcessedData)

    xtrainExisting = "trainingGEIs.pickle"    
    ytrainExisting = "trainingSubIDs.pickle"
    xtestExisting = "testingGEIs.pickle"
    ytestExisting = "testingSubIDs.pickle"
    
    existingXTrain = loadFile(xtrainExisting)
    existingYTrain = loadFile(ytrainExisting)
    existingXTest = loadFile(xtestExisting)
    existingYTest = loadFile(ytestExisting)
    
    newXTrain = np.append(xTrainNew, existingXTrain, axis = 0)
    newYTrain = np.append(yTrainNew, existingYTrain, axis = 0)
    newXTest = np.append(xTestNew, existingXTest, axis = 0)
    newYTest = np.append(yTestNew, existingYTest, axis = 0)
    
    newXTrain, newYTrain, newXTest, newYTest = shuffleFeatures(newXTrain, newYTrain, newXTest, newYTest)
    
    saveFile(newXTrain, xtrainExisting)
    saveFile(newYTrain, ytrainExisting)
    saveFile(newXTest, xtestExisting)
    saveFile(newYTest, ytestExisting)

    
    return newXTrain, newYTrain, newXTest, newYTest
    
    


# In[22]:


def callModelNewUser(preProcessedData):
    
    #Updated datasets
    X_train, X_test, y_train, y_test = addNewClass(preProcessedData)
    
    probVectorORClass = CNN(X_train, X_test, y_train, y_test) #final list of probabilities/final classification
    
    return probVectorORClass
    


# In[ ]:


def callModelExistingUser(preProcessedData):
    
    #Updated datasets
    X_train, X_test, y_train, y_test = getFeatures(preProcessedData)
    
    probVectorORClass = fcl.predict_model(X_train, X_test, y_train, y_test) #final list of probabilities/final classification
    
    return probVectorORClass
    



