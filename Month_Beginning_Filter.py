import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as BS
from matplotlib import pyplot as plt
from datetime import datetime
import statistics
import scipy.special as sp
# import fake_useragent as orange
import datetime
np.random.seed(7512)

dataframe = pd.read_excel(r"C:\Users\Dell\Desktop\Desktop\Pratyush gonna format his hardrive\DESKTOP\SEM\Semester 8\Research\Bayesian Excel Experimental Files\Significant 2005.xlsx",index_col='Date') #from quandl timeseries

#to group like how sir does
df_monthly = dataframe.reset_index().groupby([dataframe.index.year,dataframe.index.month],as_index=False).first().set_index('Date')
# df_pct_change= df_monthly.pct_change().dropna() #this is percentage change
df_pct_change = np.log(df_monthly/df_monthly.shift(1)).dropna()           #this is the log change
number_of_companies=10
weightage=100/(number_of_companies*100)
this_this = df_pct_change
this_this1=this_this.drop(columns='SENSEX')
this_this1['Profit and Loss']= this_this1.sum(axis=1)*weightage 
Total_Monthly_Profit = this_this1                                         #this gives monthly profit
this_this2 = this_this1.reset_index().groupby([this_this1.index.year],as_index=False)
Total_Yearly_Profit= this_this2.mean()[1:]                               #this gives yearly profit
Standard_Dev = this_this1.reset_index().groupby([this_this1.index.year],as_index=False).std(ddof=0)
Standard_Dev['Standard_Deviation']=Standard_Dev['Profit and Loss']
Total_Standard_Deviation = Standard_Dev[1:]
