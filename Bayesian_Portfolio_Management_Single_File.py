# In this file we will extract the data from the Quandl API and will store them locally for faster processing. The
# companies that you want to choose must be referenced with the help of documentation
import pandas as pd
from matplotlib import pyplot as plt
import quandl
import numpy as np
import scipy.special as sp

# I will be doing my work on the banks listed in BSE. Namely, Axis Bank(BOM532215), Bank of Baroda (BOM532134),
# City Union Bank (BOM532210) HDFC (BOM500180), ICICI (BOM532174), IDFC (BOM539437), Kotak Mahindra (BOM500247),
# Punjab National (BOM532461)

#This is the user's Quandl API key
quandl.ApiConfig.api_key = 'XXXXX'

# This is the start date for which you want to extract the data
start_date_set = '2002-01-01'

# This is the end date for which you want to extract the data
end_date_set = '2010-12-31'

# Change the Year to the year you want cause the total extracted data might be for multiple years
Year = 2007

#The codes below are to extract the data from Quandl. This is strictly documentation following
Axis = quandl.get('BSE/BOM532215', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                  column_index='4')
Bank_of_Baroda = quandl.get('BSE/BOM532134', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                            column_index='4')
City_Union_Bank = quandl.get('BSE/BOM532210', start_date='{}'.format(start_date_set),
                             end_date='{}'.format(end_date_set), column_index='4')
HDFC = quandl.get('BSE/BOM500180', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                  column_index='4')
ICICI = quandl.get('BSE/BOM532174', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                   column_index='4')
Kotak_Mahindra = quandl.get('BSE/BOM500247', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                            column_index='4')
Punjab_National_Bank = quandl.get('BSE/BOM532461', start_date='{}'.format(start_date_set),
                                  end_date='{}'.format(end_date_set), column_index='4')
SENSEX = quandl.get('BSE/SENSEX', start_date='{}'.format(start_date_set), end_date='{}'.format(end_date_set),
                    column_index='4')

#This is concatenating all the seperate DataFrame into one singular DataFrame
Ticker_Data = pd.concat(
    [SENSEX, Axis, Bank_of_Baroda, City_Union_Bank, HDFC, ICICI, Kotak_Mahindra, Punjab_National_Bank], axis=1)
Ticker_Data.columns = ['SENSEX', 'Axis', "Bank of Baroda", 'City Union Bank', 'HDFC', 'ICICI', 'Kotak Mahindra',
                       'Punjab National Bank']

#This is calculating the percentage change of the data that we have in Ticker_Data
Percentage_Change = Ticker_Data[
    ['SENSEX', 'Axis', "Bank of Baroda", 'City Union Bank', 'HDFC', 'ICICI', 'Kotak Mahindra',
     'Punjab National Bank']].pct_change()

# You may have extracted a lot of data for a timespan that you may not want. This code will use the timeframe that you want instead of the entire data
Sliced_Date_For_A_Year = Percentage_Change['{}-01-01'.format(Year):'{}-12-31'.format(Year)]

# Here we are calculating the loss function. A loss function of 5 means that we are penalizing overvaluation of the stocks by 5 times
k = 5
Loss_Function = 1 / (1 + k)

# Here is a function alfa_beta to calculate the up and down for the stock ticker in the selected timeframe and ultimately return the alfa and beta
def alfa_beta(
        bank):  # this will see whether the stock has risen or fallen from its previous value and attribute a score for alfa incase it has risen, or to beta incase it has decreased
    counter = 0
    up = 0
    down = 0
    while counter < len(Sliced_Date_For_A_Year): #this will make the counter euqal to the number of transactions that have occured in that particular year

        if Sliced_Date_For_A_Year.iloc[counter][bank] > Sliced_Date_For_A_Year.iloc[counter]['SENSEX']:
            up += 1 #this will take compare the pct change of the institution to the index. If the institution's pct change is greater it will add one in the variable up
        else:
            down += 1 #this will take compare the pct change of the institution to the index. If the institution's pct change is less it will add one in the variable down

        counter += 1
    alfa = 1 + up #Alfa rises by 1 when up increases by 1. Essentially it means the days when the company's stock was superior than the stock market index
    beta = 1 + down #Beta rises by 1 when down increases by 1. Essentially it means the days when the company's stock was inferiror than the stock market index
    return alfa, beta


#Here we enter the alfa and beta of all the stocks into a large DataFrame which we will refer to as 'Main_Dataframe'
Ticker_Names = ['Axis', "Bank of Baroda", 'City Union Bank', 'HDFC', 'ICICI', 'Kotak Mahindra', 'Punjab National Bank'] #We are giving this strictly for variable purposes as we require the name in the definition
Main_Dataframe = pd.DataFrame()
for items in Ticker_Names:
    list_of_ticker_names_and_their_values = ['{}'.format(items),
                                             alfa_beta('{}'.format(items))[0],
                                             alfa_beta('{}'.format(items))[1],
                                             sp.betaincinv(alfa_beta('{}'.format(items))[0],
                                                           alfa_beta('{}'.format(items))[1],
                                                           Loss_Function)]

    Sub_Main_Series = pd.Series(list_of_ticker_names_and_their_values)
    Main_Dataframe = Main_Dataframe.append(Sub_Main_Series, ignore_index=True)
Main_Dataframe.columns = ['Institution_Name', 'Alpha', 'Beta', 'Bayesian_Rank'] #This is just renaming the columns
Main_Dataframe = Main_Dataframe.sort_values('Bayesian_Rank', ascending=False)  # this sorted values from top to bottom
Main_Dataframe['Rank'] = Main_Dataframe['Bayesian_Rank'].rank(ascending=False)  # this provided Rank
Main_Dataframe
# the code works just fine upto this point

# The Code Below is to assign the weightage to the dataframe
Number_of_companies = 7
Rank_multiplier_factor = 100 / sum(range(1, Number_of_companies + 1))
Main_Dataframe['Opp_Rank'] = (Main_Dataframe['Bayesian_Rank'].rank(ascending=True)) #We changed this cause the highest rank has to be given the most weightage but according to our previous ranking it would not have been the case that is why
Main_Dataframe['Opp_Rank'] = (Main_Dataframe['Opp_Rank'] * Rank_multiplier_factor)
Main_Dataframe.rename(columns={'Opp_Rank': 'Weightage (out of 100 percentage)'}, inplace=True)
# the code works just fine upto this point

# The Code Below is to Clean the DataFrame, show the Beginning Price, Ending Price and the Year
list_of_institutions = [Axis, Bank_of_Baroda, City_Union_Bank, HDFC, ICICI, Kotak_Mahindra, Punjab_National_Bank]
Main_Dataframe['Beginning_Price'] = [x.loc['{}-01-02'.format(Year)][0] for x in list_of_institutions]
Main_Dataframe['Ending_Price'] = [x.loc['{}-12-20'.format(Year)][0] for x in list_of_institutions]
Main_Dataframe['Difference_in_Price'] = Main_Dataframe['Ending_Price'] - Main_Dataframe['Beginning_Price']
Main_Dataframe['Year'] = '{}'.format(Year)
Main_Dataframe.set_index('Rank', inplace = True)
# the code works just fine upto this point

# We are assuming that we invest 1 lac rupees at the beginning of the year to calculate the profit that we would make by using the method of Bayesian Sorting
Portfolio_Size = 100000
Main_Dataframe['Difference_in_Price'] = Main_Dataframe['Ending_Price'] - Main_Dataframe['Beginning_Price']
Main_Dataframe['Value_of_Weightage'] = Main_Dataframe['Weightage (out of 100 percentage)']/100 * Portfolio_Size
Main_Dataframe['Number_of_stock_bought_at_the_beginning_of_the_year'] = Main_Dataframe['Value_of_Weightage']/Main_Dataframe['Beginning_Price']
Main_Dataframe['Profit/ Loss'] = Main_Dataframe['Number_of_stock_bought_at_the_beginning_of_the_year']* Main_Dataframe['Difference_in_Price']
print('The total Profit/Loss by following this method of Bayesian Ranking for the Year {} is:'.format(Year),Main_Dataframe['Profit/ Loss'].sum())
#The code works just fine till this point

########### END OF CODE #########################################