# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:31:06 2019

@author: pavchemp
"""
local = False

if local:
    
    datafile = "Data/attrition.csv"
    target_col ="Attrition_new"
    attritionmodelname = "Models/attrition_model.pkl"
    survivalmodelname = "Models/survival_model.pkl"
    survivalscalername = "Models/survival_scaler.pkl"
    survivalcolumnsname = "Data/survivalcolumnnames.pkl"
    
    survival_duration_col = "YearsAtCompany"
    survival_event_col = "Attrition_numerical"
    attritionimportantfeatures="Data/attrition_importantfeatures.pkl"
    features_default_values ="Data/features_def_values.pkl"


else:
    datafile = "/home/howathon/api/Data/attrition.csv"
    target_col ="Attrition_new"
    attritionmodelname = "/home/howathon/api/Models/attrition_model.pkl"
    survivalmodelname = "/home/howathon/api/Models/survival_model.pkl"
    survivalscalername = "/home/howathon/api/Models/survival_scaler.pkl"
    survivalcolumnsname = "/home/howathon/api/Data/survivalcolumnnames.pkl"
    
    survival_duration_col = "YearsAtCompany"
    survival_event_col = "Attrition_numerical"
    attritionimportantfeatures="/home/howathon/api/Data/attrition_importantfeatures.pkl"
    features_default_values ="/home/howathon/api/Data/features_def_values.pkl"



