#!/usr/bin/env python
# coding: utf-8


from Data_Processing import *
from xgboost import plot_importance
import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from xgboost import XGBClassifier
#from sklearn.cross_validation import KFold
from sklearn.model_selection import cross_val_score
import Common as cm
from Data_Access import LoadData, StorePickle, LoadPickle

name_model = cm.attritionmodelname





# Prcocessing and Cleaning Occurs here
def process_data(data):
    data = new_features(data)
    data = conv_categories(data)
    data = gen_dummies(data)
    return data


# In[64]:


#Cross validation happens here
def cross_val_cal(fold, X, y):
    model = model_train_fit(X,y, do_fit= False)
    print(np.mean(cross_val_score(model, X, y, cv = fold, scoring= "roc_auc")))


# In[75]:


# Model in trained and model object is returned
def model_train_fit(X,y,depth = 6, l_r = 0.001, trees = 1000, sample = 0.9, do_fit = True):
    xgb = XGBClassifier(max_depth= depth, learning_rate= l_r, n_estimators= trees, subsample= sample)
    if do_fit == True:
        xgb.fit(X, y)
    return xgb


# In[66]:


# Prediction on Test Data
def predict_data(model, X_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]
    return y_pred, y_prob


# In[67]:


# Calcualte Accuracy, ROC_AUC, Precision, Recall, F1-Score
def metrics_calc(y_act, y_pred):
    print(accuracy_score(y_act, y_pred))
    print(roc_auc_score(y_act, y_pred))
    print(classification_report(y_act, y_pred))


# In[68]:


# Plotting the ROC Curve
def roc_plot(y_act, y_prob):
    
    plt.figure()
    fig_size = plt.rcParams["figure.figsize"] 
    fig_size[0] = 15
    fig_size[1] = 10
    plt.rcParams["figure.figsize"] = fig_size
    fig = plt.figure()
    fig.patch.set_facecolor('xkcd:grey')
    # Compute False postive rate, and True positive rate
    fpr, tpr, thresholds = roc_curve(y_act, y_prob)
    
    # Now, plot the computed values
    plt.plot([0, 1], [0, 1],'r--')
    plt.plot(fpr, tpr)
    plt.title("ROC CURVE")
    
    # Custom settings for the plot 
    
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('1-Specificity(False Positive Rate)')
    plt.ylabel('Sensitivity(True Positive Rate)')
    plt.legend(loc="lower right")
    plt.show()


# In[69]:


# Pandas Series with Importance of each variable
def feature_importance(model, data, train):
    imp = pd.Series(model.feature_importances_, index= data[train].columns).sort_values(ascending = False)
    print(imp)
    return imp


# In[70]:




# In[71]:


def model_load(name):
    model = LoadPickle(name)
    return model


# In[76]:

def TrainAttritionPreditorModel(filename,targetcolumn):
# Call Read Data function
    df = clean_data(LoadData(filename)) # File name should be given manually
    # Call Process Data Function
    df = process_data(df)
    # Removing the Target variable and storing ather column names
    X = list(df.drop(targetcolumn, axis=1).columns)
    y = targetcolumn
    # Splitting the Data
    X_train, X_test, y_train, y_test = train_test(df,X,y, 0.2)
    # Performing Cross Validation
    cross_val_cal(5, df[X], df[y])
    # Training the model
    model = model_train_fit(X_train, y_train)
    StorePickle(model, name_model) # Name has to be provided manually
    
    imp_ft = feature_importance(model, df, X)

    StorePickle(imp_ft, cm.attritionimportantfeatures) # Name has to be provided manually

    return model

def ModelMetrics(model, X_test,y_test):
    # Predicting with model
    y_pred, y_prob = predict_data(model, X_test)
    # Calculatinf Metrics
    metrics_calc(y_test, y_pred)
    # Plotting Roc
    roc_plot(y_test, y_prob)
    
# Getting Important Features


# In[77]:





# In[ ]:

   


def GetAttritionPredictions(df):
    df = clean_data_forprediction(df) # File name should be given manually
    # Call Process Data Function
    df = process_data(df)
    # Removing the Target variable and storing ather column names
    if (df.columns.contains(cm.target_col)):
        X = list(df.drop(cm.target_col, axis=1).columns)
        y = cm.target_col
    else:
        X = list(df.columns)
    
    # Splitting the Data
    model = model_load(name_model)
    # Predicting with model
    #print(df.columns)
    y_pred, y_prob = predict_data(model, df[X])
    return y_prob

