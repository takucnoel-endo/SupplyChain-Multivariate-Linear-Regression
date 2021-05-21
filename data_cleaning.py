# -*- coding: utf-8 -*-
"""
Data Cleaning for Supply Chain / Customer Linear Regression & Random Forest 
"""

#Import package. 
import pandas as pd
#Import files. 
df = pd.read_csv('Supplychaingdata_original.csv', encoding='latin1')
#Explore the basic file information
df.info()
#Change the column names to more intuitive names. 
#Delete Column that overlap or that are obviously insignificant. def clean_columns():
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
df.to_excel(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply Chain\SupplyChainData.xlsx', index = False)


#Import the excel dataset
df = pd.read_excel(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply Chain\SupplyChainData.xlsx')
df.info()

#Import package
import numpy as np

df_cleaning = df.copy()

#Sales data is already present in the dataset. Just in case, reassign all the values so that they are actually derived from Order_Quantity, Prod_Price, and Order_Discount
df_cleaning['Sales'] = np.nan 
df_cleaning['Sales'] = df_cleaning['Order_Quantity'] * df_cleaning['Prod_Price'] - df_cleaning['Order_Item_Discount']
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



Sports_Excercize = ['Cleats', 'Cardio Equipment', 'Shop By Sport', 'Golf Balls', 'Golf Gloves', 'Baseball & Softball', 'Hockey', 'Golf Shoes', 'Golf Apparel', 'Boxing & MMA', "Kids' Golf Clubs", 'Sporting Goods', 'Lacrosse', 'Tennis & Racquet', 'Fitness Accessories', "Men's Golf Clubs", "Women's Golf Clubs", 'Soccer', 'Strength Training', 'Basketball', 'Golf Bags & Carts']
Electronics = ['Electronics', 'Cameras', 'Computers', 'Consumer Electronics']
Clothing = ["Men's Footwear", "Women's Apparel", "Girls' Apparel", "Children's Clothing", "Women's Clothing", "Men's Clothing"]
Outdoors = ['Fishing', 'Water Sports', 'Camping & Hiking', 'Hunting & Shooting']
Recreatinal_Entertainment = ['Indoor/Outdoor Games', 'Video Games', 'Toys', 'Garden', 'DVDs', 'Music', 'Books', 'CDs']
Other = ['Trade-In', 'Pet Supplies', 'Crafts', 'Baby', 'As Seen on  TV!', 'Accessories', 'Health and Beauty']

#Before chaning the values, need to becareful of empty spaces, since above list does not take that into account. Strip all the empty spaces from the cateogory values.
df_cleaning['Cat_Name'] = df_cleaning["Cat_Name"].apply(lambda x: x.strip(' '))
#Apply lambda functions to replace all the category values based on above lists.
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Sports & Excercize' if x in Sports_Excercize else x)
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Electronics' if x in Electronics else x)
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Clothing' if x in Clothing else x)
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Outdoors' if x in Outdoors else x)
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Recreatinal & Entertainment' if x in Recreatinal_Entertainment else x)
df_cleaning['Cat_Name'] = df_cleaning['Cat_Name'].apply(lambda x: 'Other' if x in Other else x)



pd.value_counts(df_cleaning['Cat_Name']) 
#WARNING: Using for loop to process each row is not the best way to go about this, since there are about 180000 rows to iterate through. It will take foerever to run operations like that. 

#See the categories of Cust_Country
pd.value_counts(df_cleaning['Cust_Country'])
#See the categories of Cust_Type
pd.value_counts(df_cleaning['Cust_Type'])
##See the categories of Dep_Name
df.value_counts(df_cleaning['Dep_Name'])



#Order_Date and Ship_Date must be datetime dtype
def get_dates(df_column):
   #First split the value by '/' to several columns in new dataframe. 
   day = df_column.str.split(pat = '/', expand = True)
   #Also split the time values
   datetime_array = day[2].apply(lambda x: x.split(' '))
   year_array = datetime_array.apply(lambda x: x[0])
   time_array = datetime_array.apply(lambda x: x[1])
   day[3] = year_array
   day[4] = time_array
   day = day.drop(2, axis = 1)
   #Change the one 1-9 into 01-09
   day[0] = day[0].apply(lambda x: '0' + x if len(x) == 1 else x)
   day[1] = day[1].apply(lambda x: '0' + x if len(x) == 1 else x)
   #Combine date, month and year compliant to the datetime formatting and insert into the original dataframe
   df_column = day[3] + '-' + day[0] + '-' + day[1] + 'T'  + day [4]
   global new_dates
   new_dates = df_column.astype('datetime64')
#Apply the function to the dates to format them and assign them to original dataframe. 
get_dates(df_cleaning['Order_Date'])
df_cleaning['Order_Date'] = new_dates
get_dates(df_cleaning['Ship_Date'])
df_cleaning['Ship_Date'] = new_dates




#Recalculate the LeadTime_Actual based on the Order_Date and Ship_Date. 
df_cleaning['LeadTime_Actual'] = df_cleaning['Ship_Date'] - df_cleaning['Order_Date']
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].astype(str)
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].apply(lambda x: x[0]) 
df_cleaning['LeadTime_Actual'] = df_cleaning['LeadTime_Actual'].astype(float)
df_cleaning['LeadTime_Schedule'] = df_cleaning['LeadTime_Schedule'].astype(float)



#Reassign Delivery Status deriving from the calculated LeadTime_Actual and LeadTime_Schecdule
df_cleaning.loc[df_cleaning['LeadTime_Actual'] > df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "Late"
df_cleaning.loc[df_cleaning['LeadTime_Actual'] == df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "On Time"
df_cleaning.loc[df_cleaning['LeadTime_Actual'] < df_cleaning['LeadTime_Schedule'], 'Delivery_Status'] = "Advance"

#Reassign Late_Delivery_Risk deriving from the Delivery_Status.
df_cleaning.loc[df_cleaning['Delivery_Status'] == 'Late', 'Late_Delivery_Risk'] = 1
df_cleaning.loc[df_cleaning['Delivery_Status'] != 'Late', 'Late_Delivery_Risk'] = 0
df_cleaning['Late_Delivery_Risk'] = df_cleaning['Late_Delivery_Risk'].astype("category") 

#See the categories of Ship_Mode
pd.value_counts(df_cleaning.Ship_Mode)

#Export cleaned data as csv file to a specified directory. 
df_cleaning.to_csv(r'C:\Users\taku0\OneDrive\デスクトップ\DataScience\Jupyter\Linear Regression\Supply Chain\Supplychaindata_clean.csv', index = False)


#Models to create
#1. Multivariate linear regression on leat time data. 
#2. Random forest model on late delivery risk data. 
#3. Multivariate linear regression on sales data depending on customers. 
