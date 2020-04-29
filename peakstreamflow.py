
# coding: utf-8

# In[ ]:


## Created By: Kush Paliwal on 5th March 2020

## This program downloads annual peak streamflow data from USGS Surface Data Portal
## for a USER_INPUT USGS gage station
## Stores as text file (.txt) in assigned location in Jupyter Notebook

## This code is written in Python 3 format
## Import the required Modules/Packages for obtaining the data from portal

import urllib.parse
import urllib.request
import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import math


# In[ ]:


## Cell 02
## Define a function for obtaining the peak flow data from USGS Surface Data Portal
## Parameters - station number and folder name

def getpeakflow(station_number,FolderName):
    ## Building URLs
    var1 = {'site_no': station_number}
    part1 = 'https://nwis.waterdata.usgs.gov/nwis/peak?'
    part2 = '&agency_cd=USGS&format=rdb'
    link = (part1 + urllib.parse.urlencode(var1) + part2)
    print("The USGS link is: \n",link)
    
    ## Opening the link & retrieving data
    response = urllib.request.urlopen(link)
    page_data = response.read()
    
    ## File name assigning & storing the raw data as text file
    with open(FolderName + 'Data_' + station_number + '_raw' + '.txt','wb') as f1:
        f1.write(page_data)
    f1.close


# In[ ]:


## Cell 03
## Main Code

# Station No. input from user
station_number=input('Enter UHC8 Number of the required Station (USGS Station Number/site_no) \t')
print('\t')

# Store Data
FolderName='./'
peakflow_list_wb=getpeakflow(station_number,FolderName)


# In[ ]:


# Read streamflow data
data = pd.read_csv(FolderName+'Data_' + station_number + '_raw' + '.txt',skiprows=74,header=None,sep='\t',usecols=[2,4],na_filter=True,names=['Timestamp','Peak_Discharge'])
data = data.dropna()
data = data.reset_index(drop=True)

# Calculate mean and standard deviation
discharge_mean=np.mean(data['Peak_Discharge'])
discharge_sd=np.std(data['Peak_Discharge'])

# Calculate streamflow for different return periods
ReturnPeriod = [10, 25, 50, 100, 500]
StreamFlow = []

for i in ReturnPeriod:
    a = discharge_mean - (math.sqrt(6) / math.pi) * (0.5772 + math.log (math.log ( i /(i-1)))) * discharge_sd
    StreamFlow.append(a)


# In[ ]:


# Plot Flood Frequency Graph

plt.plot(ReturnPeriod,StreamFlow)
plt.xlabel('Return Period (Years)')
plt.ylabel('Discharge (cfs)')
plt.title('Flood Frequency Graph')
plt.savefig('Flood Frequency Curve.png',dpi=96, bbox_inches = "tight")

