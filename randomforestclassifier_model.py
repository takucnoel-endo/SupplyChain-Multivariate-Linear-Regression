# -*- coding: utf-8 -*-
"""
Late Delivery Risk Random Forest Classifier - Model Building / Experiementation / Hyperparameter Tuning
"""





import pandas as pd

data = pd.read_csv('Supplychaindata_clean.csv')
data.columns

mdata = data.copy()

#Choose relevant columns. 
#Delivery Risk: Pmt_Type, Cat_Name, LeadTime_Schedule, Sales, Cust_Type, Dep_Name, Cust_Region, Order_Quantity,Ship_Mode
#Inlcude all these variable into new dataset
mdata = mdata[['Pmt_Type', 'LeadTime_Schedule', 'Sales', 'Profit_Ratio', 'Cust_Type', 'Dep_Name', 'Cust_Region', 'Order_Quantity', 'Ship_Mode', 'Late_Delivery_Risk']]
mdata.columns

#Endode categorical variables using One Hot Encoding
pmt_type_dummy = pd.get_dummies(mdata['Pmt_Type'])
cust_type_dummy = pd.get_dummies(mdata['Cust_Type'])
dep_name_dummy = pd.get_dummies(mdata['Dep_Name'])
cust_region_dummy = pd.get_dummies(mdata['Cust_Region'])
ship_mode_dummy = pd.get_dummies(mdata['Ship_Mode'])
#Drop columns that were encoded
mdata1 = mdata.drop('Pmt_Type', axis = 1)
mdata1 = mdata1.drop('Cust_Type', axis = 1)
mdata1 = mdata1.drop('Dep_Name', axis = 1)
mdata1 = mdata1.drop('Cust_Region', axis = 1)
mdata1 = mdata1.drop('Ship_Mode', axis = 1)
#Merge all dummy columns into mdata
mdata1 = pd.concat([mdata1, pmt_type_dummy], axis = 1)
mdata1 = pd.concat([mdata1, cust_type_dummy], axis = 1)
mdata1 = pd.concat([mdata1, dep_name_dummy], axis = 1)
mdata1 = pd.concat([mdata1, cust_region_dummy], axis = 1)
mdata1 = pd.concat([mdata1, ship_mode_dummy], axis = 1)

pd.value_counts(mdata1.columns)

#Now just represent each categorical varaibles as numbers rather than applying One Hot Encoding. Compare the result of the final model using the normal encoding and OneHotEncoding. 
mdata2 = mdata.copy()
mdata2['Pmt_Type'] = mdata2['Pmt_Type'].apply(lambda x: 0 if x == 'CASH' else (1 if x == 'PAYMENT' else (2 if x == 'DEBIT' else 3)))
mdata2['Cust_Type'] = mdata2['Cust_Type'].apply(lambda x: 0 if x == 'Consumer' else (1 if x == 'Home Office' else 2))
mdata2['Dep_Name'] = mdata2['Dep_Name'].apply(lambda x: 0 if x == 'Fan Shop' else (1 if x == 'Golf' else (2 if x == 'Apparel' else (3 if x == 'Outdoors' else (4 if x == 'Footwear' else (5 if x == 'Fitness' else (6 if x == 'Book Shop' else (7 if x == 'Disc Shop' else (8 if x == 'Technology' else (9 if x == 'Health and Beauty' else 10))))))))))
mdata2['Cust_Region'] = mdata2['Cust_Region'].apply(lambda x: 0 if x == 'LATAM' else (1 if x == 'Europe' else (2 if x == 'Pacific Asia' else (3 if x == 'USCA' else 4))))
mdata2['Ship_Mode'] = mdata2['Ship_Mode'].apply(lambda x: 0 if x == 'Standard Class' else (1 if x == 'Second Class' else (2 if x == 'First Class' else 3)))


###############################################
#Fitting / Testing / Experimenting with Model##
###############################################

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

#Set seed before fitting the model, so we get a consistent results.
import random
random.seed(1)


#Fit the model with data with OneHot Encoding
x = mdata1.loc[:, mdata1.columns != 'Late_Delivery_Risk']
target = mdata1.loc[:, 'Late_Delivery_Risk']
   #Train-test-split
x_train, x_test, target_train, target_test = train_test_split(x, target, test_size=0.001, random_state=0)#Training:Testing - 9.999:0.001 (180338 training : 181 testing)
   #fit the model with gini 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'gini') 
clf.fit(x_train, target_train)
   #Look at the accuracy score. 
clf.score(x_test,target_test)#73.48% of the data were correctly identified with this model

   #Now fit the model with entropy. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'entropy') 
   #Look at the accuracy score. 
clf.fit(x_train, target_train)
clf.score(x_test,target_test)



#Fit the model with data with normal encoding
x = mdata2.loc[:, mdata2.columns != 'Late_Delivery_Risk']
target = mdata2.loc[:, 'Late_Delivery_Risk']
   #Train-test-split
x_train, x_test, target_train, target_test = train_test_split(x, target, test_size=0.001, random_state=0)#Training:Testing - 9.999:0.001 (180338 training : 181 testing)
   #fit the model with gini.
clf = RandomForestClassifier(n_estimators = 80, criterion = 'gini')
   #Look at the accuracy score. 
clf.score(x_test,target_test)#73.48% of the data were correctly identified with this model

   #fit the model with entropy. 
clf = RandomForestClassifier(n_estimators = 80, criterion = 'entropy') 
clf.fit(x_train, target_train)
   #Look at the accuracy score. 
clf.score(x_test,target_test)#72.92% of the data were correctly identified with this model










