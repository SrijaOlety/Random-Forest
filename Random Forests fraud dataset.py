# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:26:05 2023

@author: dell
"""

import numpy as np
import pandas as pd
df = pd.read_csv("D:\\data science python\\NEW DS ASSESSMENTS\\Random Forests\\Fraud_check.csv")
df
df.info()
df.shape

# Creating a  binary target variable based on taxable_income

df['Taxable.Income'] = df['Taxable.Income'].apply(lambda x: 'Risky' if x <= 30000 else 'Good')
df['Taxable.Income']
pd.set_option('display.max_columns', None)
df

# Preprocess the data

# EDA #

#EDA----->EXPLORATORY DATA ANALYSIS
#BOXPLOT AND OUTLIERS CALCULATION #

import seaborn as sns
import matplotlib.pyplot as plt
data = ['City.Population','Work.Experience']
for column in data:
    plt.figure(figsize=(8, 6))  
    sns.boxplot(x=df[column])
    plt.title(" Horizontal Box Plot of column")
    plt.show()
#so basically we have seen the ouliers at once without doing everytime for each variable using seaborn#

"""removing the ouliers"""

import seaborn as sns
import matplotlib.pyplot as plt
# List of column names with continuous variables
continuous_columns = ['City.Population','Work.Experience']

# Create a new DataFrame without outliers for each continuous column
data_without_outliers = df.copy()
for column in continuous_columns:
    Q1 = data_without_outliers[column].quantile(0.25)
    Q3 = data_without_outliers[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_whisker = Q1 - 1.5 * IQR
    upper_whisker = Q3 + 1.5 * IQR
    data_without_outliers = data_without_outliers[(data_without_outliers[column] >= lower_whisker) & (data_without_outliers[column] <= upper_whisker)]

# Print the cleaned data without outliers
print(data_without_outliers)
df1 = data_without_outliers
df1
# Check the shape and info of the cleaned DataFrame
print(df1.shape)
print(df1.info())

#HISTOGRAM BUILDING, SKEWNESS AND KURTOSIS CALCULATION #
df1.hist()
df1.skew()
df1.kurt()
df1.describe() 

#standardising the data

from sklearn.preprocessing import LabelEncoder
LE = LabelEncoder()
df1["Undergrad"] = LE.fit_transform(df1["Undergrad"])
df1["Marital.Status"] = LE.fit_transform(df1["Marital.Status"])
df1["Urban"] = LE.fit_transform(df1["Urban"])
df1["Taxable.Income"] = LE.fit_transform(df1["Taxable.Income"])

df1

# Split the data into features (X) and the target variable (y)

X = df1.drop("Taxable.Income", axis=1)
X
Y = df1["Taxable.Income"]
Y

#Data Partition

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y,train_size = 0.75,random_state=123)

#Random Forest  (Parallel ensemble method)

from sklearn.ensemble import RandomForestClassifier
RF = RandomForestClassifier(max_depth=9,
                        n_estimators=100,
                        max_samples=0.6,
                        max_features=0.7,
                        random_state=56)    
RF.fit(X_train,Y_train)
Y_pred_train = RF.predict(X_train)
Y_pred_test = RF.predict(X_test)

#Metrices
from sklearn.metrics import accuracy_score
ac1 = accuracy_score(Y_train,Y_pred_train)
print("Training Accuracy Score:",ac1.round(3)) 
ac2 = accuracy_score(Y_test,Y_pred_test)
print("Test Accuracy Score:",ac2.round(3)) 

#Step 1: Import the necessary libraries

from sklearn.model_selection import GridSearchCV

#Step 2: Define the parameter grid:
#we are  specifying  a dictionary where the keys are the hyperparameters we want to tune, and the values are lists of possible values for each hyperparameter. For our Random Forest model, we can consider tuning hyperparameters like max_depth, n_estimators, max_samples, and max_features.

param_grid = {
    'max_depth': [5, 10, 15],
    'n_estimators': [50, 100, 150],
    'max_samples': [0.6, 0.7, 0.8],
    'max_features': [0.6, 0.7, 0.8]
}

#Step 3: Create the GridSearchCV object
# we are creating an instance of 'Grid Search cv' class passing our random forest classifier RF and the parameter grid param_grid and and the scoring metric we want to optimize here we will take accuracy as metric.

grid_search = GridSearchCV(estimator=RF, param_grid=param_grid, scoring='accuracy', cv=5)

# here cv = 5 means it specifies 5 fold cross validation which means the data set will split into 5 parts and the model will be trained and verified 5 times.

#Step 4: Fit the GridSearchCV object to your data

grid_search.fit(X_train, Y_train)

#step 5 : getting the best hyperparameters and best model

best_params = grid_search.best_params_
best_model = grid_search.best_estimator_

# Print the best parameters found by GridSearchCV
print("Best Parameters:", grid_search.best_params_)      
# Print the best accuracy score found by GridSearchCV
print("Best Accuracy Score:", grid_search.best_score_)  
# Get the best model from the GridSearchCV
best_RF = grid_search.best_estimator_


Y_pred_train_best = best_model.predict(X_train)
accuracy_best = accuracy_score(Y_train, Y_pred_train_best)
print("Best Model Train Accuracy:", accuracy_best)

Y_pred_test_best = best_model.predict(X_test)
accuracy_best = accuracy_score(Y_test, Y_pred_test_best)
print("Best Model Test Accuracy:", accuracy_best)



