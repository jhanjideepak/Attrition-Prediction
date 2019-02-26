# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 13:08:49 2019

@author: pavchemp
"""
import pandas as pd
import pickle

def LoadData(filename):
    data = pd.read_csv(filename)
    return data


def StoreData(data, filename):
    data.to_csv(filename, index=False)
    return "Data saved"




def LoadPickle(name):
    model_pkl = open(name, 'rb')
    model = pickle.load(model_pkl)
    print("Loaded model :: ", model)
    return model



# # Dump Model to Pickle
# Pickle is a Python libraries which is the best choice to perform the task like
# - Pickling  the process converting any Python object into a stream of bytes by following the hierarchy of the object we are trying to convert. 
# - Unpickling the process of converting the pickled (stream of bytes) back into to the original Python object by following the object hierarchy

def StorePickle(model, name):
    model_pkl = open(name, 'wb')
    pickle.dump(model, model_pkl)
    model_pkl.close()


