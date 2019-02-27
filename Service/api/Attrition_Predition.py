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



def GetAttritionPredictionswithreason(df):
    df = clean_data_forprediction(df) # File name should be given manually
    # Call Process Data Function
    df = process_data(df)
    # Removing the Target variable and storing ather column names
    if (df.columns.contains(cm.target_col)):
        df = df.drop(cm.target_col, axis=1)
    X = list(df.columns)
    # Splitting the Data
    model = model_load(name_model)
    # Predicting with model
    #print(df.columns)
    y_pred, y_prob = predict_data(model, df[X])
    df["Attrition"] = y_pred
    df["Probability"] = y_prob
    df["ProbableReason"] = df.apply(GetProbableReasons, axis = 1)
    select = ["Probability","Attrition","ProbableReason"]
    df["Probability"] = df['Probability'].apply(lambda x:round(x,2))
    df["Attrition"] = df['Attrition'].apply(lambda x:"Yes" if x==1 else "No")
    return df[select]



# In[77]:

def GetAverageValuesForImportantFeatures(df):
    imp_feat = LoadPickle(cm.attritionimportantfeatures)
    top_feat = pd.DataFrame(imp_feat.head(10))
    print(top_feat)
    top_feat = top_feat.reset_index()
    top_feat.columns = ['feature_name','p']
    top_feat["avg_value"] = 0
    top_feat["std_dev"] = 0
    values = []
    df_n = df[df.Attrition_Yes==1]
    df = df[df.Attrition_Yes==0]
    for eachfeat in top_feat.feature_name:
        print(eachfeat)
        avg = df[eachfeat].median()
        top_feat.at[top_feat["feature_name"]==eachfeat,"avg_value"] = avg
        top_feat.at[top_feat["feature_name"]==eachfeat,"std_dev"] = df[eachfeat].std()
        top_feat.at[top_feat["feature_name"]==eachfeat,"attrition_avg_value"] = df_n[eachfeat].median()
        top_feat.at[top_feat["feature_name"]==eachfeat,"attrition_std_dev"] = df_n[eachfeat].std()

    return top_feat


# In[77]:

def GetProbableReasons(row):
    reason_feat = ""
    if row["Attrition"] == 1:
        imp_feat_val = LoadPickle(cm.features_default_values)
        imp_feat_val["current_val"] = 0
        imp_feat_val["distance"] = 0
        for eachfeat in imp_feat_val.feature_name:
            if row.index.contains(eachfeat):
                row_val = row[eachfeat]
                imp_feat_val.at[imp_feat_val["feature_name"]==eachfeat,"current_val"] = row_val
                feat_avg_val = imp_feat_val[imp_feat_val["feature_name"]==eachfeat].avg_value.values[0]
                feat_stddev = imp_feat_val[imp_feat_val["feature_name"]==eachfeat].std_dev.values[0]  
                attr_avg_val = imp_feat_val[imp_feat_val["feature_name"]==eachfeat].attrition_avg_value.values[0]
                distance_1 = np.sqrt(np.square( row_val - feat_avg_val))
                distance_2 = np.sqrt(np.square(row_val-attr_avg_val))
                min_dist = min([distance_1, distance_2])
                if (min_dist == distance_2):
                    imp_feat_val.at[imp_feat_val["feature_name"]==eachfeat,"distance"] =min_dist
                
            
        imp_feat_val['temp']= imp_feat_val['distance']/imp_feat_val['attrition_std_dev']
        
        reason_feat = imp_feat_val[imp_feat_val["temp"]==max(imp_feat_val['temp'])].feature_name.values[0]
    return reason_feat 
            
        
 