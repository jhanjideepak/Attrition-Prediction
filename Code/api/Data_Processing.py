#!/usr/bin/env python
# coding: utf-8

# # People Attrition
# 
# The analytic methods can improve Human Resources (HR) management for companies with large number of employees. It is very easy to give example, how can companies benefit from machine learning methods applied to HR. Let’s assume that training of new employee costs 1000 dollars and if we can predict which employee is going to leave next month, and propose him/her a bonus program worth 500 dollars to keep him for next 6 months, we are 500 dollars on plus and keep experienced, well-trained employee under the hood, with higher morale.
# 

# ### Importing Necessary Libraries

# In[1]:


import warnings
warnings.filterwarnings('ignore')


# In[2]:


import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from scipy import stats
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import Imputer

# ### Setting Working Directory

# In[3]:


# Function to change Working Directory and list elements present in new working directory
def set_wd(wd):
    print(os.getcwd())
    os.chdir(wd)
    return(os.listdir())


# ### Data Exploration

# In[4]:


# Function Explore the data: Number of Rows, Columns, Data Types of Columns
def explore(df):
    print('The input dataset df','has',df.shape[0],"rows and",df.shape[1],'columns') #Printing Shape
    print("The summary of Numeric Columns:")
    print(df.describe())
    print("The type of variables in the input dataset are ")
    print(df.dtypes) # Prints Columns Data Type
    print("Null values in each column")
    print(df.isnull().sum()) # Checking Number of Null values in each columns
    print("Number of unique values in each Column")
    print(df.nunique()) # Checking Number of unique Values in each columns


# ### Deleting Columns with Zero Variability

# In[5]:


# Removing Columns with 0 variance i.e containing only single values
def del_zero_var_cols(data):
    a = dict(data.nunique())
    for i,j in a.items():
        if j == 1:
            data.drop(i, axis = 1, inplace = True)
    return data


# ### Split Data into Categorical and Continuous

# In[6]:


# Split Categorical and Continuous Variables in a Dataframe based on Number of Unique values present in Columns
def split_cat_count(df, cat_cols):
    
    df_cat = df[cat_cols] # Creating Separate Data frame of Categorical Variables
    df_cont = df.drop(cat_cols, axis=1) # Creating Data frame of Continuous Varables
    return df_cat, df_cont


# ### Data Scaling

# In[7]:


# This function accepts Dataframe and Columns which needs to be scaled and return the full data frame with scaled variables
#Pass Columns in form of list
# data -: Dataframe, 
# Cols :list of column names whichneeds scaling
def scale_data(data, cols, way = "standard"):     
    if way == "min_max":# If min max scaling is used in "way" argumtn
        scale = MinMaxScaler()
        temp = scale.fit_transform(data[cols].values)
        temp = pd.DataFrame(temp, columns= cols, index= data.index)
        data[cols] = temp[cols]
    elif way == "standard":# If Standard Scaling is passed in "way" argument
        scale = StandardScaler()
        temp = scale.fit_transform(data[cols].values)
        print(scale.mean_)
        temp = pd.DataFrame(temp, columns= cols, index= data.index)
        data[cols] = temp[cols]
    return data


# ### Missing Value Treatment For Continuous Data

# In[8]:


# This function treates missing values of Continuous data with the help of above mentioned Imputation Techniques
def missing_val_treatment_cont(df_cont, way = "mean"):
    if way == "mean": # Replace all Null values by column means (Valid only for Numeirc Variables)
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp.fit(df_cont)#Fit Imputer to data
        X = pd.DataFrame(imp.transform(df_cont), columns= df_cont.columns, index= df_cont.index)# Fill the NULL values
    elif way == "median":# Replace all Null values by column medians (Valid only for Numeirc Variables)
        imp = Imputer(missing_values='NaN', strategy='median', axis=0)
        imp.fit(df_cont)
        X = pd.DataFrame(imp.transform(df_cont), columns= df_cont.columns, index= df_cont.index)
    elif way == "ffill":# Replace all Null values by Next value present
        X = df_cont.fillna(method = "ffill")
    elif way == "bfill":# Replace all Null values by Previous value present
        X = df_cont.fillna(method = "bfill")  
    return X


# In[9]:


# #### -> Impute Missing values using machine learning Algorithm
# This function uses fancyimpute library to Impute missing values of Numeric Data. The fancy impute uses machine learning algorithms to impute missing values.
def impute_fancy(df, way = "knn"):#Only valid for numeric Data
    if way == "knn":# If you want to fill missing values using "KNN" algorithm
        df_numeric = df2.select_dtypes(include=[np.float])
        df_filled = pd.DataFrame(KNN(5).complete(df_numeric.as_matrix()), columns= df_numeric.columns, index= df_numeric.index)
    
    elif way == "mice": #If you want to fill missing values using "MICE" algorithm
        df_numeric = df2.select_dtypes(include=[np.float])
        df_filled = pd.DataFrame(mice.complete(df_numeric.as_matrix()), columns= df_numeric.columns, index= df_numeric.index)
    
    return df_filled


# ### Missing Value Treatment For Categorical Data

# In[207]:


# This function treates missing values of Catgoerical data with the Mode of that particular feature
def missing_val_treatment_cat(df_cat):
    for i in df_cat.columns:
        df_cat[i].fillna(stats.mode(df_cat[i])[0][0], inplace = True)
    return df_cat


# ### Preparing Final Data by combining Continuous and Categorical

# In[235]:


def combine_cat_cont(df_cat, df_cont):
    final_data = pd.concat([df_cat, df_cont], axis=1)
    return final_data


# In[10]:

def gen_dummies(data):
    data = pd.get_dummies(data, drop_first= True)
    return data    



def train_test(df, X, y, size):
    X_train, X_test, y_train, y_test = train_test_split(df[X], df[y], test_size=size)
    return X_train, X_test, y_train, y_test


# ### Encoding and Bucketing the Features

# In[193]:


# This function creates derived variables and delete older ones which are used to create this. It takes data frame as input.
# data -: Data frame
def new_features(data):
    edu_field = {"Life Sciences": 1, "Medical": 2, "Marketing": 3, "Technical Degree": 4, "Other": 5, "Human Resources": 6}
    job_role = {"Sales Executive": 1, "Research Scientist": 2, "Laboratory Technician": 3, "Manufacturing Director": 4, "Healthcare Representative": 5,               "Manager":6, "Sales Representative":7, "Research Director": 8, "Human Resources":9}
    
    # Encoding Object Variables
    data["job_role"] = data["JobRole"].map(job_role)
    data["edu_field"] = data["EducationField"].map(edu_field)
    data["Gender"] = data["Gender"].apply(lambda x: 1 if x == "Male" else 2)
    data["mar_status"] = data["MaritalStatus"].apply(lambda x: 1 if x == "Single" else (2 if x == "Married" else 3))
    data["travel"] = data["BusinessTravel"].apply(lambda x: 2 if x == "Travel_Rarely" else (3 if x == "Travel_Frequently" else 1))
    
    if (data.columns.contains("Attrition")):
        data["Attrition_new"] = data["Attrition"].apply(lambda x: 1 if x == "Yes" else 0)
        data["Attrition_new"] = data["Attrition_new"].astype("category", categories = [0,1])
    
    data["Department_new"] = data["Department"].apply(lambda x: 1 if x == "Research & Development" else (2 if x == "Sales" else 3))
    data["over_time"] = data["OverTime"].apply(lambda x: 1 if x == "No" else 2)
    
    #Bucketing the Variables after exploring
    data["Education_level"] = data["Education"].apply(lambda x: 1 if (x==1 or x==2) else (3 if (x==4 or x==5) else 2))
    data["Env_satisfaction"] = data["EnvironmentSatisfaction"].apply(lambda x: 1 if x==1 else (2 if (x==2) else 3))
    data["job_involve"] = data["JobInvolvement"].apply(lambda x: 1 if x==1 else (2 if (x==2) else 3))
    data["job_satisfaction"] = data["JobSatisfaction"].apply(lambda x: 1 if (x == 1 or x == 2) else 2)
#     data["num_companies_worked"] = data["NumCompaniesWorked"].apply(lambda x: 1 if (x == 0 or x == 1) else (2 if (x >= 2 and x <= 4) else 3))
#     data["hike"] = data["PercentSalaryHike"].apply(lambda x: 1 if (x >= 0 and x < 11) else (2 if (x >= 11 and x < 16) else 3))
    data["stock_level"] = data["StockOptionLevel"].apply(lambda x: 1 if (x <= 1) else 2)
#     data["trainings_taken"] = data["TrainingTimesLastYear"].apply(lambda x: 1 if (x < 3) else 2)
#     data["time_last_promotion"] = data["YearsSinceLastPromotion"].apply(lambda x: 1 if (x < 1) else (2 if (x >= 1 and x < 3) else 3))
#     data["time_curr_manager"] = data["YearsWithCurrManager"].apply(lambda x: 1 if (x < 3) else (2 if (x >= 3 and x < 8) else 3))
#     data["curr_role_tenure"] = data["YearsInCurrentRole"].apply(lambda x: 1 if (x <= 3) else 2)
                                                       
    if (data.columns.contains("Attrition")):
        data.drop("Attrition", axis = 1, inplace = True)
        
    data = data.drop(["EducationField","Department", "Education", "EnvironmentSatisfaction", "JobInvolvement", "JobSatisfaction", "StockOptionLevel",  "BusinessTravel", "MaritalStatus", "JobRole", "OverTime"], axis = 1)

    #"TrainingTimesLastYear", "YearsSinceLastPromotion", "YearsWithCurrManager",              "YearsInCurrentRole",
#     data = data.drop(["EducationField", "Attrition", "Department", "Education", "EnvironmentSatisfaction", "JobInvolvement", "JobSatisfaction", "NumCompaniesWorked",\
#              "PercentSalaryHike", "StockOptionLevel", "TrainingTimesLastYear", \
#              "BusinessTravel", "MaritalStatus", "JobRole", "OverTime"], axis = 1)
#     data = data.drop(["JobRole", "EducationField","MaritalStatus", "BusinessTravel", "Attrition", "Department", "OverTime"], axis = 1)
    return data


# ### Ensuring the Categories of Features for Test Data

# In[208]:


# This funciton converts colmns into Categories so that if there is an unseen data during test, our model works fine
def conv_categories(data):
    
    data["job_role"] = data["job_role"].astype("category", categories = [1,2,3,4,5,6,7,8,9])
    data["edu_field"] = data["edu_field"].astype("category", categories = [1,2,3,4,5,6])
    data["Gender"] = data["Gender"].astype("category", categories = [1,2])
    data["mar_status"] = data["mar_status"].astype("category", categories = [1,2,3])
    data["travel"] = data["travel"].astype("category", categories = [1,2,3])
    data["Department_new"] = data["Department_new"].astype("category", categories = [1,2,3])
    data["over_time"] = data["over_time"].astype("category", categories = [1,2])
    data["Education_level"] = data["Education_level"].astype("category", categories = [1,2,3])
    data["Env_satisfaction"] = data["Env_satisfaction"].astype("category", categories = [1,2,3])
    data["job_involve"] = data["job_involve"].astype("category", categories = [1,2,3])
    data["job_satisfaction"] = data["job_satisfaction"].astype("category", categories = [1,2])
#     data["num_companies_worked"] = data["num_companies_worked"].astype("category", categories = [1,2,3])
#     data["hike"] = data["hike"].astype("category", categories = [1,2,3])
    data["stock_level"] = data["stock_level"].astype("category", categories = [1,2])
    data["JobLevel"] = data["JobLevel"].astype("category", categories = [1,2,3,4,5])
#     data["trainings_taken"] = data["trainings_taken"].astype("category", categories = [1,2])
#     data["time_last_promotion"] = data["time_last_promotion"].astype("category", categories = [1,2,3])
#     data["time_curr_manager"] = data["time_curr_manager"].astype("category", categories = [1,2,3])
#     data["curr_role_tenure"] = data["curr_role_tenure"].astype("category", categories = [1,2])


#     data["JobLevel"] = data["JobLevel"].astype("category", categories = [1,2,3,4,5])
#     data["WorkLifeBalance"] = data["WorkLifeBalance"].astype("category", categories = [1,2,3,4])
#     data["RelationshipSatisfaction"] = data["RelationshipSatisfaction"].astype("category", categories = [1,2,3,4])
#     data["Education"] = data["Education"].astype("category", categories = [1,2,3,4,5])
#     data["EnvironmentSatisfaction"] = data["EnvironmentSatisfaction"].astype("category", categories = [1,2,3,4])
#     data["JobInvolvement"] = data["JobInvolvement"].astype("category", categories = [1,2,3,4])
#     data["JobSatisfaction"] = data["JobSatisfaction"].astype("category", categories = [1,2,3,4])
#     data["StockOptionLevel"] = data["StockOptionLevel"].astype("category", categories = [0,1,2,3])
    
    
    data["WorkLifeBalance"] = data["WorkLifeBalance"].astype("category", categories = [1,2,3,4])
    data["RelationshipSatisfaction"] = data["RelationshipSatisfaction"].astype("category", categories = [1,2,3,4])
    return data




# ### Generating Dummy Variables

# In[209]:


# Function reads the Data, removes unwanted columns
def clean_data(df):    
    df.drop("EmployeeNumber", axis=1, inplace= True)
    df.drop("PerformanceRating", axis= 1, inplace= True)
    df = del_zero_var_cols(df)
    return df



def clean_data_forprediction(df):   
    if (df.columns.contains("EmployeeNumber")):
        df.drop("EmployeeNumber", axis=1, inplace= True)
    if (df.columns.contains("PerformanceRating")):
        df.drop("PerformanceRating", axis= 1, inplace= True)
    if (df.columns.contains("StandardHours")):
        df.drop("StandardHours", axis= 1, inplace= True)
    if (df.columns.contains("EmployeeCount")):
        df.drop("EmployeeCount", axis= 1, inplace= True)
          
    return df