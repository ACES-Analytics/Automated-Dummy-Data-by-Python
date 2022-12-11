# -*- coding: UTF-8 -*-
"""
This script is to create dummy sales records for analytics purpose
Created on Fri Dec 8 15:14:00 2022
@author ACES ANALYTICS TEAM

"""

## 1. Import modules and packages

import numpy as np
import pandas as pd
from faker import Faker
import random, os, string
from pandas import DataFrame
from random import seed, choice, randint
import datetime
from datetime import datetime, timedelta
from time import strftime, localtime
from pytz import timezone
import pytz
import matplotlib
matplotlib.use("Qt5Agg")  # Do this before importing pyplot.
import matplotlib.pyplot as plt
plt.close("all")

fake = Faker()

## 2. Define number variables
num_ctry = 10 # number of fake countries
num_cust = 50 # number of fake customers
num_dates = 3000 # number of fake dates
num_slmn = 30 # number of fake salesman

## 3. Import local file - material master data
# path, r'D:\Python\ACES_Analytics\ACES001\Input'
df_mtl_md = pd.read_excel(r'D:\Python\ACES_Analytics\ACES001\Input\ACES001_Material Master Data.xlsx')

## 4. Generate fake customer, country, salesman, salesteam
# Generate fake customer
cust = [fake.unique.company() + " " + fake.company_suffix() for i in range(num_cust)]

# Generate fake country
ctry = [fake.unique.country() for i in range(num_ctry)]
ctry2 = [fake.word(ext_word_list = ctry) for i in range(num_cust)]

# Generate fake salesman
slmn = [fake.unique.name() for i in range(num_slmn)]
slmn2 = [fake.word(ext_word_list = slmn) for i in range(num_cust)]

# Generate fake sales team
sl_team = ['Team One','Team Two','Team Three','Team Four']
sl_team2 = [fake.word(ext_word_list = sl_team) for i in range(num_slmn)]

# Generate fake customer master data with country salesman info
df_cust = pd.DataFrame({"Customer": cust,"Country": ctry2, "Salesman":slmn2},index = range(num_cust))

# Generate Salesman dataframe with sales team info
df_slmn = pd.DataFrame({"Salesman": slmn,"Sales Team": sl_team2})

# Get sales team info to df_cust
df_cust2 = pd.merge(df_cust,df_slmn,on="Salesman")

## 5. Generate time series of three years

# Generate fake random date
import datetime
dates = [fake.date_between(datetime.date(2019, 1, 1), datetime.date(2021, 12, 31)) for i in range (num_dates)]
# Convert dates list into pandas dataframe
df_dates = pd.DataFrame({"raw_date":dates})

# Convert data type from Object to Datetime
df_dates['Date'] = pd.to_datetime(df_dates['raw_date'])

# Find day of week
df_dates['raw_day'] = df_dates['Date'].dt.day_name()

# Convert data type from object to String
df_dates['raw_day'].astype('string')

# Get abbreviation of day of week
df_dates['Day'] = (df_dates['raw_day'].apply(lambda x: x[0:3]))

# Delete rows for day = Sat and Sun
df_dates2 = df_dates.query("Day != 'Sun' and Day != 'Sat'")

# Get length of dataframe
df_len = len(df_dates2 )
print(df_len)

# Slice df_dates3 for easily reference purpose
df_dates3 = df_dates2.loc[:,['Date','Day']]

## 6. Generate sales records
# Generate customers records with length of the above dates records
cust2 = [fake.word(ext_word_list = cust) for i in range(df_len)]

df_dates3['Customer'] = cust2

# Get country, salesman, sales team info for df_dates3
df_dates4 = pd.merge(df_dates3,df_cust2,on="Customer")

# Generate sales volumn
df_dates4['Sales Volumn'] = pd.DataFrame(np.random.randint(1000,5000,df_len))

# Sort df_dates5 by dates
df_dates5 = df_dates4.sort_values(by="Date")

# Change data type of date from datetime to string
df_dates5['Date'].astype('string')

# Change date format as YYY-MM-DD
df_dates5['Date'] = (df_dates5['Date'].apply(lambda x: x.strftime("%Y-%m_%d")))

# Convert material text column into list
Mtl_text = df_mtl_md.loc[:,'Mtl Text' ].tolist()

# Generate material records with same length of dates
Mtl_text2 = [fake.word(ext_word_list = Mtl_text) for i in range(df_len)]

# Generate one column for Mtl Text info
df_dates5['Mtl Text'] =  Mtl_text2

# Slice df_mtl_text for join purpose
df_mtl_md2 = df_mtl_md.loc[0:, ["Mtl Text", "Mtl Code", "Profit Center", "Mtl Grp","Unit", "Ave Price\n($)"]]

# Join master data info of Mtl Text into df_dates5  to generate final sales records
df_sales = pd.merge(df_dates5,df_mtl_md2,on="Mtl Text")

# Excluding wrong country data
df_sales.loc[df_sales['Country'] == "Hong Kong",'Country'] = "Beautiful Country"

## 7. Export data to excel file
# Export data to excel without index
# Path: r'D:\Python\ACES_Analytics\ACES001\Output''
df_sales.to_excel(r'D:\Python\ACES_Analytics\ACES001\Output\ACES001_Sales Records.xlsx', index = False)

# Print the end for this script
print("The run of script is completed successfully.")

# Print time now

time_local = strftime ("%A, %d %b %Y, %H:%M")
print(time_local)
