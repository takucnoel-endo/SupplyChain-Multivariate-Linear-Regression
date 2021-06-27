# -*- coding: utf-8 -*-
"""
Late Delivery Risk Random Forest Classifier - Model Building / Experiementation / Hyperparameter Tuning
"""

from time import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import random
from sklearn.model_selection import GridSearchCV
import time

#Function to create a starting dataframe. 
def read_data(directory):
   data = pd.read_csv(directory)
   mdata = data.copy()
   #Choose relevant columns. 
   mdata = mdata[['Pmt_Type', 'LeadTime_Schedule', 'Sales', 'Profit_Ratio', 'Cust_Type', 'Dep_Name', 'Cust_Region', 'Order_Quantity', 'Ship_Mode', 'Late_Delivery_Risk']]
   columns = data.columns
   mcolumns = mdata.columns
   return data, mdata, columns, mcolumns

#Function to apply onehot encoding, and create a modified dataframe based on columns created by onehot encoding.  
def OneHot(data):
   pmt_type_dummy = pd.get_dummies(data['Pmt_Type'])
   cust_type_dummy = pd.get_dummies(data['Cust_Type'])
   dep_name_dummy = pd.get_dummies(data['Dep_Name'])
   cust_region_dummy = pd.get_dummies(data['Cust_Region'])
   ship_mode_dummy = pd.get_dummies(data['Ship_Mode'])
   #Drop columns that were encoded
   data_onehot = data.drop('Pmt_Type', axis = 1)
   data_onehot = data_onehot.drop('Cust_Type', axis = 1)
   data_onehot = data_onehot.drop('Dep_Name', axis = 1)
   data_onehot = data_onehot.drop('Cust_Region', axis = 1)
   data_onehot = data_onehot.drop('Ship_Mode', axis = 1)
   #Merge all dummy columns into mdata
   data_onehot = pd.concat([data_onehot, pmt_type_dummy], axis = 1)
   data_onehot = pd.concat([data_onehot, cust_type_dummy], axis = 1)
   data_onehot = pd.concat([data_onehot, dep_name_dummy], axis = 1)
   data_onehot = pd.concat([data_onehot, cust_region_dummy], axis = 1)
   data_onehot = pd.concat([data_onehot, ship_mode_dummy], axis = 1)
   return data_onehot

#Function to just represent each categorical varaibles as numbers rather than applying One Hot Encoding. Compare the result of the final model using the normal encoding and OneHotEncoding. 
def standard_category(data):
   data_standard = data.copy()
   data_standard['Pmt_Type'] = data_standard['Pmt_Type'].apply \
               (lambda x: 0 if x == 'CASH' else (1 if x == 'PAYMENT' else (2 if x == 'DEBIT' else 3)))
   data_standard['Cust_Type'] = data_standard['Cust_Type'].apply \
               (lambda x: 0 if x == 'Consumer' else (1 if x == 'Home Office' else 2))
   data_standard['Dep_Name'] = data_standard['Dep_Name'].apply \
               (lambda x: 0 if x == 'Fan Shop' else (1 if x == 'Golf' else (2 if x == 'Apparel' else \
                     (3 if x == 'Outdoors' else (4 if x == 'Footwear' else (5 if x == 'Fitness' else \
                     (6 if x == 'Book Shop' else (7 if x == 'Disc Shop' else (8 if x == 'Technology' else \
                     (9 if x == 'Health and Beauty' else 10))))))))))
   data_standard['Cust_Region'] = data_standard['Cust_Region'].apply \
               (lambda x: 0 if x == 'LATAM' else (1 if x == 'Europe' else \
                     (2 if x == 'Pacific Asia' else (3 if x == 'USCA' else 4))))
   data_standard['Ship_Mode'] = data_standard['Ship_Mode'].apply \
               (lambda x: 0 if x == 'Standard Class' else (1 if x == 'Second Class' else (2 if x == 'First Class' else 3)))
   return data_standard

def separate_x_target(data, target_column):
   x = data.loc[:, data.columns != target_column]
   target = data.loc[:, target_column]
   return x, target

#Function for fitting the model and getting the model score with normal validation method. 
def fit_get_score(model, x_train, target_train, x_test, target_test): 
   model.fit(x_train, target_train)
   return model.score(x_test, target_test)



##################
###Main Program###
##################
df_original, df_model, columns, mcolumns = read_data(directory = 'C:\\Users\\taku0\\OneDrive\\デスクトップ\\Data Science\\Supply Chain\\Supplychaindata_clean.csv')
onehot_data = OneHot(data = df_model)
standard_data = standard_category(data = df_model)



#Fitting / Testing / Experimenting with Model (One Hot Data)
onehot_x, onehot_target = separate_x_target(data = onehot_data, target_column = 'Late_Delivery_Risk')
   #Train-test-split since the dataset is extremely large, and also random forest algorythm rarely overfit to the training dataset, we can get away with having a smal proportion of dataset as the testing set. Testing set will still have approximately 100 datapoints. 
x_train, x_test, target_train, target_test = train_test_split(onehot_x, onehot_target, test_size=0.001, random_state=0)#Training:Testing - 9.999:0.001 (180338 training : 181 testing)
   #fit the model with gini / get accuracy score. 80 different trees are found to be optimal when considering trade-off between prediction accurracy and training speed, and also after 80 trees, the model does not seem to improve much. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'gini', max_features = 4) 
fit_get_score(clf, x_train, target_train, x_test, target_test) 
   #fit the model with gini / get accuracy score. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'entropy', max_features = 4) 
fit_get_score(clf, x_train, target_train, x_test, target_test)



#Fitting / Testing / Experimenting with Model (Standard Encoded Data)
standard_x, standard_target = separate_x_target(standard_data, 'Late_Delivery_Risk')
   #Train-test-split
x_train, x_test, target_train, target_test = train_test_split(standard_x, standard_target, test_size=0.001, random_state=0)#Training:Testing - 9.999:0.001 (180338 training : 181 testing)
   #fit the model with gini / get accuracy score. 80 different trees are found to be optimal when considering trade-off between prediction accurracy and training speed, and also after 80 trees, the model does not seem to improve much. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'gini', max_features = 'Auto') 
fit_get_score(clf, x_train, target_train, x_test, target_test)
   #fit the model with gini / get accuracy score. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'entropy', max_features = 'Auto') 
fit_get_score(clf, x_train, target_train, x_test, target_test) 


#Use GridSearh method to choose the best hyperparameters.
   #Initialize classifier.
clf = RandomForestClassifier()
   #Initialize hyper-parameter grids dictionary. 
param_grid = {
    'n_estimators': [60, 80, 100],
    'max_features': ['auto', 'sqrt', 'log2'],
    'criterion': ['gini', 'entropy']
}
   #Create grid search object using the initialized classifier and the hyperparameter grids, 10 folds cross validation.
CV_clf = GridSearchCV(estimator = clf, param_grid = param_grid, cv = 10)
   #Fit the model. Choose the data with onehot encoding.
print('Running Grid Search...')
start = time.time()
CV_clf.fit(onehot_data, onehot_target)
end = time.time()
print('Runtime:', end-start)
   #Print best parameters. 
best_param = CV_clf.best_params_ #{'criterion': 'gini', 'max_features': 'auto', 'n_estimators': 60}

x_train, x_test, target_train, target_test = train_test_split(onehot_x, onehot_target, test_size=0.001, random_state=0)
clf = RandomForestClassifier(n_estimators = best_param['n_estimators'], criterion = best_param['criterion'], max_features = best_param['max_features'])
fit_get_score(clf, x_train, target_train, x_test, target_test)