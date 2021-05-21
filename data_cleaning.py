# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#Import package. 
import pandas as pd
#Import files. 
df = pd.read_csv('DataCoSupplyChainDataset.csv', encoding='latin1')
#Explore the basic file information
df.info()
#Change the column names to more intuitive names. 
#Delete Column that overlap or that are obviously insignificant. 
df.rename(columns={'Type': 'Pmt_Type'}, inplace=True)
df.rename(columns={'Days for shipping (real)': 'LeadTime_Actual'}, inplace=True)
df.rename(columns={'Days for shipment (scheduled)': 'LeadTime_Schedule'}, inplace=True)
df = df.drop('Sales', axis = 1)
df.rename(columns={'Sales per customer': 'Sales'}, inplace=True)
df.rename(columns={'Category Name': 'Cat_Name'}, inplace=True)
df = df.drop('Category Id', axis = 1)
df.rename(columns={'Customer City': 'Cust_City'}, inplace=True)
df.rename(columns={'Customer Country': 'Cust_Country'}, inplace=True)
df = df.drop('Customer Email', axis = 1)
df = df.drop('Customer Fname', axis = 1)
df = df.drop('Customer Lname', axis = 1)
df = df.drop('Customer Password', axis = 1)
df.rename(columns={'Customer Segment': 'Cust_Type'}, inplace=True)
df = df.drop('Customer State', axis = 1)
df = df.drop('Customer Street', axis = 1)
df = df.drop('Customer Zipcode', axis = 1)
df.rename(columns={'Market': 'Cust_Region'}, inplace=True)
df = df.drop('Department Id', axis = 1)
df.rename(columns={'Department Name': 'Dep_Name'}, inplace=True)
df = df.drop('Latitude', axis = 1)
df = df.drop('Longitude', axis = 1)
df = df.drop('Order City', axis = 1)
df = df.drop('Order Country', axis = 1)
df = df.drop('Order Region', axis = 1)
df = df.drop('Order State', axis = 1)
df = df.drop('Order Status', axis = 1)
df = df.drop('Order Zipcode', axis = 1)
df.rename(columns={'Order Customer Id': 'Cust_ID'}, inplace=True)
df.rename(columns={'order date (DateOrders)': 'Order_Date'}, inplace=True)
df.rename(columns={'shipping date (DateOrders)': 'Ship_Date'}, inplace=True)
df.rename(columns={'Order Id': 'Order_ID'}, inplace=True)
df = df.drop('Order Item Cardprod Id', axis = 1)
df = df.drop('Product Card Id', axis = 1)
df = df.drop('Order Item Discount Rate', axis = 1)
df.rename(columns={'Order Item Id': 'Order_ID'}, inplace=True)
df.rename(columns={'Order Item Product Price': 'Prod_Price'}, inplace=True)
df.rename(columns={'Order Item Profit Ratio': 'Profit_Ratio'}, inplace=True)
df.rename(columns={'Order Item Quantity': 'Order_Quantity'}, inplace=True)
df = df.drop('Order Item Total', axis = 1)
df.rename(columns={'Order Profit Per Order': 'Order_Profit'}, inplace=True)
df = df.drop('Product Category Id', axis = 1)
df = df.drop('Product Description', axis = 1)
df = df.drop('Product Image', axis = 1)
df = df.drop('Product Price', axis = 1)
df = df.drop('Product Status', axis = 1)
df.rename(columns={'Shipping Mode': 'Ship_Mode'}, inplace=True)
df.rename(columns={'Delivery Status': 'Delivery_Status'}, inplace=True)
df.rename(columns={'Late_delivery_risk': 'Late_Delivery_Risk'}, inplace=True)
df.info()
#Export into excel file to make the dataset more structured, for example, the order od columns. 
df.to_excel(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply ChainFile SupplyChainData.xlsx', index = False)


#Import the excel dataset
df = pd.read_excel(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply ChainFile SupplyChainData.xlsx')
df.info()

#Import package
import numpy as np


df.rename(columns={'Order Item Discount': 'Order_Discount'}, inplace=True)

df_cleaning = df

#Sales data is already present in the dataset. Just in case, reassign all the values so that they are actually derived from Order_Quantity, Prod_Price, and Order_Discount
df_cleaning['Sales'] = np.nan 
df_cleaning['Sales'] = df_cleaning['Order_Quantity'] * df_cleaning['Prod_Price'] - df_cleaning['Order_Discount']
#Profit Ratio data is already present in the dataset. Just in case, reassign all the values so that they are actually derived from Order_Profit and Sales
df_cleaning['Profit_Ratio'] = df_cleaning['Order_Profit']/df_cleaning['Sales']

#See Cat_Name categories. Any unwanted categories? 
pd.value_counts(df_cleaning['Cat_Name']) #There are many categories that overlap with each other. 
#I'll try my best judgement to reassign these vategories into more general groupings. 

#Categories...
#1. Sports/Excercize
#2. Electronics
#3. Clothing
#4. Outdoors
#5. Accesories
#6. Recreatinal/Entertainment
#7. Health/Cosmetics
#8. Other

Sports_Excercize = ['Cleats', 'Cardio Equipment', 'Shop By Sport', 'Golf Balls', 'Golf Gloves', 'Baseball & Softball', 'Hockey', 'Golf Shoes', 'Golf Apparel', 'Boxing & MMA', 'Kids Golf Clubs', 'Sporting Goods', 'Lacrosse', 'Tennis & Racquet', 'Fitness Accessories', 'Mens Golf Clubs', 'Womens Golf Clubs', 'Soccer', 'Strength Training', 'Basketball', 'Golf Bags & Carts']
Electronics = ['Electronics', 'Cameras', 'Computers', 'Consumer Electronics']
Clothing = ['Mens Footwear', 'Womens Apparel', 'Girls Apparel', 'Childrens Clothing', 'Womens Clothing', 'Mens Clothing']
Outdoors = ['Fishing', 'Water Sports', 'Camping & Hiking', 'Hunting & Shooting']
Recreatinal_Entertainment = ['Indoor/Outdoor Games', 'Video Games', 'Toys', 'Garden', 'DVDs', 'Music', 'Books', 'CDs']
Other = ['Trade-In', 'Pet Supplies', 'Crafts', 'Baby', 'As Seen on  TV!', 'Accessories', 'Health and Beauty']


for i in range(df_cleaning.shape[0]):
   if (df_cleaning.loc[i, 'Cat_Name'] in Sports_Excercize): 
      df_cleaning.loc[i, 'Cat_Name'] = 'Sports_Excercize'
   elif (df_cleaning.loc[i, 'Cat_Name'] in Electronics): 
      df_cleaning.loc[i, 'Cat_Name'] = 'Electronics'
   elif (df_cleaning.loc[i, 'Cat_Name'] in Clothing): 
      df_cleaning.loc[i, 'Cat_Name'] = 'Clothing'
   elif (df_cleaning.loc[i, 'Cat_Name'] in Outdoors): 
      df_cleaning.loc[i, 'Cat_Name'] = 'Outdoors'
   elif (df_cleaning.loc[i, 'Cat_Name'] in Recreatinal_Entertainment): 
      df_cleaning.loc[i, 'Cat_Name'] = 'Recreatinal_Entertainment'
   else:
      df_cleaning.loc[i, 'Cat_Name'] = 'Other'
pd.value_counts(df_cleaning['Cat_Name']) 
#WARNING: Using for loop to process each row is not the best way to go about this, since there are about 180000 rows to iterate through. It will take foerever to run operations like that. 

#See the categories of Cust_Country
pd.value_counts(df_cleaning['Cust_Country'])
#See the categories of Cust_Type
pd.value_counts(df_cleaning['Cust_Type'])
##See the categories of Dep_Name
df.value_counts(df_cleaning['Dep_Name'])


#Order_Date and Ship_Date must be datetime dtype
#First split the value by '/' to several columns in new dataframe. 
oday = df_cleaning['Order_Date'].str.split(pat = '/', expand = True)
sday = df_cleaning['Ship_Date'].str.split(pat = '/', expand = True)
#get rid of the time value in the last columns
oday[2] = oday[2].str[0:4]
sday[2] = sday[2].str[0:4]
#Change the one 1-9 into 01-09
oday[0] = oday[0].apply(lambda x: '0' + x if len(x) == 1 else x)
oday[1] = oday[1].apply(lambda x: '0' + x if len(x) == 1 else x)
sday[0] = sday[0].apply(lambda x: '0' + x if len(x) == 1 else x)
sday[1] = sday[1].apply(lambda x: '0' + x if len(x) == 1 else x)
#Combine date, month and year compliant to the datetime formatting and insert into the original dataframe
oday['Order_Date'] = oday[2] + '-' + oday[0] + '-' + oday[1]
sday['Ship_Date'] = sday[2] + '-' + sday[0] + '-' + sday[1]
#Add the new Order_date and Ship_Date to the original dataset. Change the dtype to datetime
df_cleaning['Order_Date'] = oday['Order_Date']
df_cleaning['Ship_Date'] =sday['Ship_Date']
df_cleaning['Order_Date'] = df_cleaning['Order_Date'].astype('datetime64')
df_cleaning['Ship_Date'] = df_cleaning['Ship_Date'].astype('datetime64')


#See the categories of Ship_Mode
pd.value_counts(df_cleaning.Ship_Mode)

#Recalculate the LeadTime_Actual based on the Order_Date and Ship_Date. 
df_cleaning['LeadTime_Actual'] = df_cleaning['Ship_Date'] - df_cleaning['Order_Date']
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].astype(str)
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].apply(lambda x: x.strip(x[-4:]))
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].astype(int)

#Reassign Delivery Status deriving from the calculated LeadTime_Actual and LeadTime_Schecdule
df_cleaning.loc[df_cleaning['LeadTime_Actual'] > df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "Late"
df_cleaning.loc[df_cleaning['LeadTime_Actual'] == df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "On Time"
df_cleaning.loc[df_cleaning['LeadTime_Actual'] < df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "Advance"

#Reassign Late_Delivery_Risk deriving from the Delivery_Status.
df_cleaning.loc[df_cleaning['Delivery_Status'] == 'Late', 'Late_Delivery_Risk'] = 1
df_cleaning.loc[df_cleaning['Delivery_Status'] != 'Late', 'Late_Delivery_Risk'] = 0


#Export cleaned data as csv file to a specified directory. 
df_cleaning.to_csv(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply Chain\Supplychaindata_clean.csv', index = False)
