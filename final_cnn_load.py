from __future__ import print_function
import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.models import model_from_json 
import numpy as np
from scipy import stats
import pickle



def predict_model(input):
    print(input.shape)
    #formatting shape
    #input = input.reshape((1,128, 88, 1)).astype(np.float32)
    input = np.expand_dims(input,axis = 3)
    input /= 255
    #input = np.expand_dims(input,axis=0)
    print(input.shape)

    #load model
    json_file = open('./model_40.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("./model_40.h5")

    loaded_model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])

    #predict using loaded model
    data = loaded_model.predict(input)
    
    #get subject id
    label_train = pickle.load(open("./trainingSubIDs.pickle",'rb'))
    label_train = np.asarray(label_train)
    sorted = np.unique(label_train)
    
    #find index of max prediction
    x = stats.mode(np.argmax(data, axis=1))
    prediction = sorted[x[0]]
    print(prediction)
    return prediction
