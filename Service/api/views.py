# -*- coding: utf-8 -*-
"""
Created on Tue Jul 03 10:57:33 2018

@author: Paviya. Utkarsh
"""

#from flask import render_template,Request
#from api import app
import pandas as pd
import json
import datetime
import os
from flask import jsonify, request, abort, Response
import numpy as nm
import requests
#os.chdir("E:/HSBC/TicketPrediction/app")
dir = "D:\\Howathon\\Code"
#os.chdir(dir)
from flask_cors import CORS
from Attrition_Predition import GetAttritionPredictions, TrainAttritionPreditorModel,GetAttritionPredictionswithreason
from Survival_Analysis import PredictSurvivalFunction
from Data_Access import LoadData, StoreData, LoadPickle
import Common as cm
from flask import Flask

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def get_default():
    return "Welcome to attrition prediction service!"

@app.route("/health")
def get_health():
    return "Health OK"




@app.route("/GetHistoricalData" , methods=['GET'])
def GetHistoricalData():
    try:
        data = LoadData(cm.datafile)
        out_json = data.to_json(orient="records")

        return out_json
    except Exception as e:
        raise e
        abort(500)          
        

@app.route("/GetAttritionPrediction" , methods=['GET','POST'])
def GetAttritionPrediction():
    try:
        data = request.get_json(force = True)
        #postreqdata = json.loads(data)
        #print(type(postreqdata))
        df = pd.DataFrame(data)
        print(df.columns)
        pred = GetAttritionPredictions(df)
        #out_json = pred.to_json(orient="records")
        print(pred)
        return json.dumps(pred.tolist())
    except Exception as e:
        raise e
        abort(500)          

@app.route("/GetAttritionPredictionwithreason" , methods=['POST'])                
def GetAttritionPredictionwithreason():
    try:
        data = request.get_json(force = True)
        #postreqdata = json.loads(data)
        #print(data)
        df = pd.DataFrame(data)
        print(df.columns)
        pred = GetAttritionPredictionswithreason(df)
        out_json = pred.to_json(orient="records")
        #print(pred)
        return out_json#json.dumps(pred.tolist())
    except Exception as e:
        raise e
        abort(500)                         
        

@app.route("/GetDashboardData" , methods=['GET'])
def GetDashboardData():
    try:
        data = LoadData(cm.datafile)
        features = LoadPickle(cm.attritionimportantfeatures)
        select = ['Age','NumCompaniesWorked', 'DistanceFromHome','MonthlyIncome','Attrition','YearsSinceLastPromotion']
        data = data[select]
        out_json = data.to_json(orient="records")

        return out_json
    except Exception as e:
        raise e
        abort(500)            
        
@app.route("/GetSurvivalData" , methods=['POST'])
def GetSurvivalData():
    try:
        data = request.get_json(force = True)
        #postreqdata = json.loads(data)
        #postreqdata = json.loads(request.data.decode('utf-8'))
        #print(type(postreqdata))
        df = pd.DataFrame(data)        
        data = PredictSurvivalFunction(df)
        out_json = data.to_json(orient="records")

        return out_json
    except Exception as e:
        raise e
        abort(500)     


@app.route("/RetrainAttritionPredictionModel" , methods=['POST'])
def RetrainAttritionPredictionModel():
    try:
        data = request.get_json(force = True)
        #postreqdata = json.loads(data)
        #postreqdata = json.loads(request.data.decode('utf-8'))
        #print(type(postreqdata))
        df = pd.DataFrame(data)      
        #Commenting temporarily to avoid overwriting the file
        #StoreData(df, cm.datafile)
        TrainAttritionPreditorModel(cm.datafile, cm.target_col)
        return "Success"
    except Exception as e:
        raise e
        abort(500)     


        
if __name__ == '__main__':
    app.run()
   

       
