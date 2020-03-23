#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import final_cnn_load as fcl

def findGEI(preProcessedData):
    
    GEIs = []
    testDf = pd.DataFrame()
    testDf = pd.DataFrame.from_dict(preProcessedData, dtype = 'uint32')
    
    for d in preProcessedData:
        tempArr = np.asarray(d.get("cycleImgs"))
        GEIs.append(np.mean(tempArr, axis = 0))
        
    subIds = testDf['usr_id'].to_numpy(dtype = 'int32')
    
    return GEIs, subIds


# In[2]:


from sklearn.model_selection import train_test_split

def getFeatures(preProcessedData):
    
    combinedGEIs, subIds = findGEI(preProcessedData)
    
    X_train, X_test, y_train, y_test = train_test_split(combinedGEIs, subIds, test_size=0.30, random_state=42)
    
    return X_train, X_test, y_train, y_test


# In[3]:


def callModel(preProcessedData):
   if preProcessedData.get("usr_id") == 0:
       GEI, _ = findGEI(preProcessedData)
       return fcl.predict_model(GEI)
   else:
        X_train, X_test, y_train, y_test = getFeatures(preProcessedData)
        return 10009
#    probVectorORClass = CNN(X_train, X_test, y_train, y_test) #final list of probabilities/final classification
    
#    return probVectorORClass
    

