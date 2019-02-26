# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 23:23:24 2019

@author: pavchemp
"""
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from lifelines import CoxPHFitter
from sklearn import preprocessing
import app.Common as cm
from app.Data_Access import LoadData, StorePickle, LoadPickle

survivalModelName = cm.survivalmodelname
scalerName = cm.survivalscalername
scalerColumnNames = cm.survivalcolumnsname



def PreprocessDataforModelling(df):
    target_map = {'Yes':1, 'No':0}
# Using the pandas apply method to numerically encode our attrition target variable
    df["Attrition_numerical"] = df["Attrition"].apply(lambda x: target_map[x])
    df = pd.get_dummies(df,drop_first=True)# drop_first=True should be used
    df.drop(['Attrition_Yes'], axis=1, inplace=True)
    df.replace([np.inf, -np.inf], np.nan, inplace = True)
    scaler = preprocessing.StandardScaler()
    names = df.columns

    scaled_data = scaler.fit_transform(df)
    scaled_data = pd.DataFrame(scaled_data, columns=names)
    scaled_data.drop(['StandardHours','EmployeeCount'], axis = 1, inplace = True)
    StorePickle(scaler,scalerName )
    StorePickle(names,scalerColumnNames)
    return scaled_data

def PreprocessDataforPrediction(df):
    target_map = {'Yes':1, 'No':0}
# Using the pandas apply method to numerically encode our attrition target variable
    if df.columns.contains('Attrition'):
        df["Attrition_numerical"] = df["Attrition"].apply(lambda x: target_map[x])
    df = pd.get_dummies(df,drop_first=True)# drop_first=True should be used
    if df.columns.contains('Attrition_Yes'):
        df.drop(['Attrition_Yes'], axis=1, inplace=True)
    #df.replace([np.inf, -np.inf], np.nan, inplace = True)
    scaler = LoadModel(scalerName)
    scalernames = LoadModel(scalerColumnNames)
    names = df.columns
    missingnames = set(scalernames).difference(set(names))
    if len(missingnames)>0:
        for eachname in missingnames:
            df[eachname]=0
    names = df.columns
    scaled_data = scaler.transform(df)
    scaled_data = pd.DataFrame(scaled_data, columns=names)
    scaled_data.drop(['StandardHours','EmployeeCount'], axis = 1, inplace = True)
    return scaled_data


def TrainModel(df, durationcol=cm.survival_duration_col, eventcol=cm.survival_event_col):
    cph = CoxPHFitter()   ## Instantiate the class to create a cph object
    cph.fit(df, duration_col=durationcol,show_progress=True, event_col=eventcol)
    return cph



def SaveModel(model):
    StorePickle(model, survivalModelName)


def LoadModel(modelname):
    return LoadPickle(modelname)

def TrainSurvivalAnalysisModel():
    data = LoadData(cm.datafile)
    data = PreprocessDataforModelling(data)
    cph_model = TrainModel(data,cm.survival_duration_col,cm.survival_event_col)
    SaveModel(cph_model)
    
    
def PredictSurvivalFunction(new_data):
    cph = LoadModel(survivalModelName)
    data = PreprocessDataforPrediction(new_data)
    survival = cph.predict_survival_function(data, times=[0.5, 1, 2])
    return survival.T


    
    