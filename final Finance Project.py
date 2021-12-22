#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython.display import display, Math, Latex

import pandas as pd
import numpy as np
import numpy_financial as npf
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime


# ## Group Assignment
# ### Team Member Names: Stephen Chen, Bhavya Shah, Alex Liu
# ### Team Strategy Chosen: RISKY Portfolio

# In[2]:


# Importing csv file with tickers and reformatting dataframe
ticker_list = pd.read_csv("Sample Tickers.csv")
add_columns = pd.DataFrame({ticker_list.columns[0]:ticker_list.columns[0]}, index=[len(ticker_list)])
ticker_list = ticker_list.append(add_columns)
ticker_list.columns=['Tickers']


# In[3]:


# displaying the list of tickers
ticker_list


# In[4]:


# identifying American stocks, converting tickers to American (if possible)
for i in range(0, len(ticker_list)):
    ticker = str(ticker_list.iloc[i, 0])
    
    # finds the period in the stock tickers
    get_position = ticker.find('.')
    
    # if there is a period in the string (meaning that it's not an American stock)
    if (get_position != -1):
        ticker_list.iloc[i, 0] = ticker[:get_position]


# In[5]:


sector_list = pd.DataFrame(columns = ['Sectors'])

# function that determines the standard deviation of each stock
def get_deviation(ticker):
    stock_ticker = ticker
    stock_hist = stock_ticker.history(start='2019-01-01', end='2021-07-01')
    stock_close = stock_hist['Close']
    
    # grouping Close prices by months
    stock_close.index = pd.to_datetime(stock_close.index)
    monthly_close = stock_close.groupby(stock_close.index.to_period('m')).head(1)

    # returning the standard deviation based off of percent change
    return (monthly_close.pct_change()*100).std()

i = 0

for i in range (len(ticker_list)):
    stock = yf.Ticker(ticker_list.iloc[i, 0])
    sector = stock.info.get('sector')
    add_data = pd.DataFrame({'Sectors':sector,
                             'Standard Deviation': get_deviation(stock)},index=[i])
    sector_list = sector_list.append(add_data)


# In[6]:


sector_list


# In[7]:


ticker_list = pd.concat([ticker_list, sector_list], join='inner',axis=1)


# In[8]:


ticker_list = ticker_list[ticker_list.Sectors.notnull()]
ticker_list.set_index('Sectors', inplace=True)


# In[9]:


ticker_list


# In[10]:


# dropping stocks that have insufficient data

# creating a duplicate ticker list to transform
duplicate_list = ticker_list.copy()

# resetting the index of the duplicate list
duplicatelist.reset_index(inplace=True)

# list of indices to drop later
drop = []


# In[11]:


# Apple is a company that has sufficient stock information. We use Apple as a reference for how many entries of information a stock should have.

# getting the ticker, history and close price information of Apple
apple = yf.Ticker('AAPL')
apple_hist = apple.history(start="2019-01-01", end="2021-01-01")
apple_close = apple_hist['Close']

# getting the length of the Close Price of Apple Dataframe (this is how much data should be in each dataframe)
desired_length = len(apple_close)


# In[12]:


# for-loop to check each stock to see if they have a sufficient amount of data
for i in range (0, len(ticker_list)):
    
    # getting the ticker, ticker history and close price information of each stock.
    ticker = yf.Ticker(ticker_list.iloc[i, 0])
    t_hist = ticker.history(start="2019-01-01", end="2021-01-01")
    ticker_close = t_hist['Close']
    
    # if there is an insufficient amount of data, append to the list of indices to be dropped
    if (len(ticker_close) != desired_length):
        drop.append(duplicate_list.index[i])


# In[13]:


# dropping the stocks with an insufficient amount of information
duplicate_list.drop(drop, inplace=True)

# re-indexing and re-formatting the duplicate dataframe
duplicate_list.index = duplicate_list['Sectors']
duplicate_list.drop(columns=['Sectors'], inplace=True)

# removing the undesired stocks from the ticker list
ticker_list = duplicate_list


# In[14]:


# displaying the ticker list
ticker_list


# In[15]:


# placeholder volume column
ticker_list["Volume"] = None

# loop to calculate the average daily volume of each stock
for i in range (0, len(ticker_list)):
    
    # getting the number of days between June 2, 2021 and October 22, 2021
    num_days = int(str(pd.to_datetime('2021-07-02') - pd.to_datetime('2021-10-22'))[1:4])
    
    # getting each ticker's information
    ticker = yf.Ticker(ticker_list.iloc[i, 0])
    ticker_hist = ticker.history(start="2021-07-02", end="2021-10-22")
    ticker_volume = ticker_hist['Volume'].sum()/num_days
    ticker_list.iloc[i, -1] = ticker_volume
    
# filtering for the tickers that fit our requirement
ticker_list = ticker_list[(ticker_list["Volume"] > 10000)]


# In[16]:


def sort_list (industry_list, industry):
    industry_list = ticker_list.filter(like = industry, axis=0)
    industry_list = industry_list.sort_values(by=['Standard Deviation'], ascending = False)
    return industry_list
    


# In[17]:


energy_list = sort_list (ticker_list, 'Energy')
energy_list


# In[18]:


financial_list = sort_list (ticker_list, 'Financial Services') 
financial_list


# In[19]:


tech_list = sort_list (ticker_list, 'Technology')
tech_list


# In[20]:


healthcare_list = sort_list (ticker_list, 'Healthcare')
healthcare_list


# In[21]:


estate_list = sort_list (ticker_list, 'Real Estate')
estate_list


# In[22]:


industry_list = sort_list (ticker_list, 'Industrials')
industry_list


# In[23]:


utilities_list = sort_list(ticker_list, 'Utilities')
utilities_list


# In[24]:


communication_list = sort_list(ticker_list,'Communication Services')
communication_list


# In[25]:


materials_list = sort_list(ticker_list,'Basic Materials')
materials_list


# In[26]:


consumer_list = sort_list(ticker_list,'Consumer Defensive')
consumer_list


# In[27]:


# getting the list of the sectors
sectors_list = [energy_list, financial_list, tech_list, healthcare_list, estate_list, industry_list, utilities_list, communication_list, materials_list, consumer_list]


# In[28]:


# filter out sectors without any stocks
filtered_sectors_list = []

# for-loop to get rid of any sectors without any stocks in them (lowers run-time)
for i in range (0, len(sectors_list)):
    
    # if the sector list isn't empty, add the sector to the filtered list
    if (len(sectors_list[i]) != 0):
        filtered_sectors_list.append(sectors_list[i])


# In[29]:


# find the sector with the highest standard deviation
def find_highest_sector_deviation(list_of_sectors):
    
    sector_deviation = []
    
    # list of sectors isn't empty
    if (len(list_of_sectors) != 0):
        
        # temporary variables for the highest deviation, along with the sector with the highest deviation
        highest_deviation = -100000000
        highest_deviation_sector = None
    
        # for-loop which loops through each sector
        for i in range (0, len(list_of_sectors)):
    
            # temporary dataframe to store values
            temp = pd.DataFrame()
    
            # dataframe with each stock in a specific sector
            sector = list_of_sectors[i]
            
            # getting the average deviation of each stock/standard deviation of the sector
            temp_deviation = sector['Standard Deviation'].sum()/len(sector)
    
            # determining if that sector has the highest deviation or not, if it is, change the values
            if (temp_deviation > highest_deviation):
                highest_deviation = temp_deviation
                highest_deviation_sector = sector
                
            sector_deviation.append([sector.index[0], temp_deviation])
        
        # return the sector with the highest deviation
        return highest_deviation_sector, sector_deviation
    
    # list of sectors is empty
    else:
        
        # return 0
        return 0


# In[30]:


filtered_sectors_list


# In[31]:


filtered_sectors_list[3]


# In[32]:


high_deviation_sector = find_highest_sector_deviation(filtered_sectors_list)[0]
high_deviation_sector


# In[33]:


new_filtered = []

for i in range (0, len(filtered_sectors_list)):
    if (filtered_sectors_list[i].index[0] != high_deviation_sector.index[0]):
        new_filtered.append(filtered_sectors_list[i])

new_filtered


# In[34]:


energy_list


# In[66]:


def get_correlations(sector, sector_list):
    
    # creating temporary lists to transform later
    returned_list = [sector]
    correlation_list = []
    
    # creating an empty dataframe for now
    sector_df = pd.DataFrame()
    
    # filling up the sector monthly returns
    for i in range (0, len(sector)):
        
        # getting ticker name, ticker history, weighted close price
        sector_ticker = yf.Ticker(sector.iloc[i, 0])
        sector_history = sector_ticker.history(start='2019-01-01', end='2021-01-01')
        sector_close_price = sector_history['Close']
        
        # converting to monthly data
        sector_close_price.index = pd.to_datetime(sector_close_price.index)
        sector_monthly_close_price = sector_close_price.groupby(sector_close_price.index.to_period('m')).head(1)
        sector_df['Monthly Close Price of ' + sector.iloc[i,0]] = sector_monthly_close_price
        
    # calculating value of sector (as if it were a portfolio), monthly returns and standard deviation
    sector_df['Value of Sector'] = sector_df.sum(axis=1)
    sector_df['Monthly Returns'] = sector_df['Value of Sector'].pct_change()*100
    sector_df = sector_df['Monthly Returns']
        
    # getting the correlations of the rest of the sectors
    for j in range (0, len(sector_list)):
        
        # temporary dataframe to store values
        temp = pd.DataFrame()
        correlation = pd.DataFrame()
    
        # dataframe with each stock in a specific sector
        init_sector = sector_list[j]
    
        # for-loop for each stock in a sector
        for k in range (0, len(init_sector)):
            # getting ticker name, ticker history, weighted close price
            ticker = yf.Ticker(init_sector.iloc[k, 0])
            history = ticker.history(start='2019-01-01', end='2021-01-01')
            close_price = history['Close']
            
            # converting to monthly data
            close_price.index = pd.to_datetime(close_price.index)
            monthly_close = close_price.groupby(close_price.index.to_period('m')).head(1)
            
            temp['Monthly Close Price of ' + init_sector.iloc[k,0]] = monthly_close
                
        # calculating value of sector (as if it were a portfolio), monthly returns and standard deviation
        temp['Value of Sector'] =  temp.sum(axis=1)
        temp['Monthly Returns'] = temp['Value of Sector'].pct_change()*100
        temp = temp['Monthly Returns']
        
        # concatenating the sector dataframe along with the dataframe of the other sector
        combined = pd.concat([sector_df, temp], join='inner', axis=1)
        
        # calculating the correlation and extracting the correlation
        correlation = combined.corr().iloc[0, 1]
        
        # appending the correlation, along with the sector name to a list
        correlation_list.append([init_sector.index[0], correlation, sector_list[j]])
    
    # sorting the list with the sectors and correlation information from greatest to least
    correlation_list.sort(key=lambda x: x[1], reverse=True)
    
    # appending the sectors with the highest correlations to a separate list
    for l in range (0, len(correlation_list)):
        correlation_sector = correlation_list[l]
        returned_list.append(correlation_sector[2])
    
    # returning the data
    return returned_list


# In[67]:


# list with sectors in an descending correlative order
list_of_corr = (get_correlations(high_deviation_sector, new_filtered))

# displaying the list
list_of_corr


# After finding the standard deviation of each sector, we decided to use the sector with the highest standard deviation as a foundation for our portfolio, then built the rest of the portfolio around that sector. To elaborate, we first included all the stocks from the sector with the highest standard deviation in the portfolio, as it should be the sector with the riskiest stocks. Furthermore, since all the stocks are from the same sector, they should be fairly positively correlated. As a result, we will have a group of risky stocks that generally move in the same direction, so the risk of the overall portfolio will increase. Then, we found the correlation of all the sectors with each other, as shown above. We sorted the rest of the sectors by their correlation with the riskiest sector, from highest positive correlation to negative correlation.
# 
# Next, we added stocks from the most positively correlated sectors from the sorted list to the portfolio until we had 10 stocks in the portfolio. The result can be seen from the ticker_list dataframe below, where we include all the stocks from a sector before moving on to the next sector. This limits the amount of sectors we have in our portfolio, and since all the sectors are as positively correlated as possible, the amount of inter-industry diversification is limited as well. To reiterate, we tried to include the least amount of sectors in our portfolio as possible by including all the stocks from the riskiest sectors. As a result, our portfolio becomes more prone to risk that is specific to the industries that we have in our portfolio. Moreover, we selected the sectors that have the highest positive correlation with the riskiest sector, so the stocks in the portfolio will generally move in the same direction, further increasing risk. We decided to only have 10 stocks in our portfolio as we wanted to have the least amount of stocks as possible, to limit the amount of diversification. With less stocks in our portfolio, each stock will have a greater influence on the performance of the overall portfolio, thus increasing risk. In the case that we could not include an entire sector in our portfolio due to the limit of 10 stocks, the stocks with the highest standard deviation were added to our portfolio, maximizing the risk of the portfolio.

# In[40]:


ticker_list = pd.concat(list_of_corr)


# In[41]:


ticker_list = ticker_list[:10]
ticker_list


# In[42]:


def get_returns (ticker):
    stock = yf.Ticker(ticker)
    start_date = '2019-01-01'
    end_date = '2021-11-01'
    history = stock.history(start=start_date, end=end_date)
    prices = pd.DataFrame({ticker: history['Close']})
    prices = prices.resample('MS').ffill()
    prices = prices.pct_change()
    return prices

get_returns ('OXY')

#return_list = get_returns(ticker_list.iloc[0,0])


# In[43]:


return_list = get_returns(ticker_list.iloc[0,0])


# In[44]:


i = 1
for i in range (len(ticker_list)):
    ticker = ticker_list.iloc[i,0]
    add_returns = get_returns (ticker)
    return_list = pd.concat([return_list, add_returns], join = 'inner', axis = 1)


# In[45]:


return_list = return_list.iloc[: , 1:]


# In[46]:


return_list


# In[47]:


corr = return_list.corr()
corr


# In[48]:


highest_corr = pd.DataFrame({'test':corr[corr.columns[0]].nlargest(2)})
highest_corr


# After deciding on the 10 stocks for our portfolio, we needed to decide on how much of the portfolio to allocate to each stock. In order to create the riskiest portfolio, we needed to invest most of our money into the least amount of stocks as possible. To accomplish this, we invested 35 percent of the portfolio in the stock from the riskiest sector with the highest standard deviation. As mentioned earlier, standard deviation is a direct measure of risk, so the stock with the highest standard deviation should be the riskiest. Then, we invested 25 percent in the stock that is the most positively correlated with the stock with the highest standard deviation, as shown above. By doing this, we would invest 25 percent of our money in the stock that is the most directly related to riskiest stock. We invested 25 percent of our money in this stock as it was the most we could, since we needed to invest at least 5000 dollars in each stock to meet the requirements. As a result, we have 60 percent of our portfolio allocated to the 2 riskiest stocks that are positively correlated to each other, and 5 percent of our portfolio in each of the 8 other stocks. By having 60 percent of our portfolio in 2 stocks, we allowed the returns of the portfolio to be primarily determined by 2 stocks. Hence, we greatly limited the amount of diversification by increasing exposure to the risk of the 2 stocks, which in turn, increases the risk of the portfolio. As for the 8 other stocks, if they are highly positively correlated with the first 2 stocks, then they will further increase the risk the portfolio. On the other hand, if they have a lower correlation with the first 2 stocks, it won't affect the risk of the portfolio by too much, as we only invested 5 percent in each of these stocks. 

# In[49]:


def stock_df (ticker, value, num):
    myhistory = yf.Ticker(ticker).history(start='2021-05-19', end='2021-11-30', interval= '1d')
    data= {'Ticker': ticker,
           'Price': myhistory.loc['2021-11-24', 'Close'],
           'Shares': value/myhistory.loc['2021-11-24', 'Close'],
           'Values': value, 'Weight (Percent)': [value/1000]}
    grades= pd.DataFrame(data,index=[num])
    return grades

stock1 = stock_df (highest_corr.index[0], 35000, 1)
stock2 = stock_df (highest_corr.index[1], 25000, 2)


# In[50]:


ticker_list = ticker_list[ticker_list.Tickers != highest_corr.index[0]]


# In[51]:


ticker_list = ticker_list[ticker_list.Tickers != highest_corr.index[1]]


# In[52]:


ticker_list


# In[53]:


FinalPortfolio = stock1.append(stock2)

i = 0
for i in range (8):
    add_stock = stock_df(ticker_list.iloc[i,0], 5000, i+3)
    FinalPortfolio = FinalPortfolio.append(add_stock)
    
total = pd.DataFrame({'Ticker': 'N/A',
                      'Price': 'N/A',
                      'Shares': 'N/A',
                      'Values': sum(FinalPortfolio.Values),
                      'Weight (Percent)': sum(FinalPortfolio['Weight (Percent)'])}, index=[11])


# In[54]:


FinalPortfolio = FinalPortfolio.append(total)


# In[55]:


FinalPortfolio


# In[56]:


FinalPortfolio.drop(FinalPortfolio.tail(1).index,inplace=True)


# In[57]:


FinalPortfolio.reset_index(inplace=True)


# In[58]:


FinalPortfolio


# In[59]:


Stocks = pd.concat([FinalPortfolio['index'], FinalPortfolio['Ticker'], FinalPortfolio['Shares']], join='inner',axis=1)
Stocks.columns=['','Ticker','Shares']


# In[60]:


Stocks


# In[61]:


# prints out the final CSV file with all
Stocks.to_csv('Stocks_Group_16.csv', encoding='utf-8', index=False)


# In[62]:


# getting the monthly returns of each sector
def find_returns(df):
    
    # sectors without any tickers inside of them
    if (len(df) == 0):
        return None
    
    # sectors with tickers inside of them
    else:
        
        # creating a temporary dataframe
        init_frame = pd.DataFrame(columns=['Close Prices'])
        
        # getting the ticker, ticker history and close price
        init_ticker = yf.Ticker(df.iloc[0,0])
        init_hist = init_ticker.history(start="2019-01-01", end="2021-01-01")
        init_close = init_hist['Close']
        
        # converting the daily data to monthly data
        init_close.index = pd.to_datetime(init_close.index)
        monthly_init_close = init_close.groupby(init_close.index.to_period('m')).head(1)
        init_frame['Close Prices'] = monthly_init_close
        
        # if there is only one stock in the sector
        if (len(df) == 1):
            init_frame['Monthly Returns'] = init_frame['Close Prices'].pct_change()*100
            return init_frame['Monthly Returns']
    
        else:
            # looping through the sectors to get the monthly returns
            for i in range (1, len(df)):
                
                # getting the ticker, ticker history and close price history
                ticker = yf.Ticker(df.iloc[i, 0])
                ticker_hist = ticker.history(start="2019-01-01", end="2021-01-01")
                ticker_close = ticker_hist['Close']
                
                # converting the daily data to monthly data
                ticker_close.index = pd.to_datetime(ticker_close.index)
                monthly_close = ticker_close.groupby(ticker_close.index.to_period('m')).head(1)
            
                # adding the close prices of each stock
                init_frame['Close Prices'] = init_frame['Close Prices'] + monthly_close
        
                # calculating the monthly returns
                init_frame['Monthly Returns'] = init_frame['Close Prices'].pct_change()*100
        
            # returning the monthly returns
            return init_frame['Monthly Returns']
    
    return 1


# In[63]:


correlation = pd.DataFrame()
correlation['Energy Monthly Returns (%)'] = find_returns(energy_list)
correlation['Financial Services Monthly Returns (%)'] = find_returns(financial_list)
correlation['Technology Monthly Returns (%)'] = find_returns(tech_list)
correlation['Healthcare Monthly Returns (%)'] = find_returns(healthcare_list)
correlation['Real Estate Monthly Returns (%)'] = find_returns(estate_list)
correlation['Industrials Monthly Returns (%)'] = find_returns(industry_list)
correlation['Utilities Monthly Returns (%)'] = find_returns(utilities_list)
correlation['Communication Services Monthly Returns (%)'] = find_returns(communication_list)
correlation['Materials Monthly Returns (%)'] = find_returns(materials_list)
correlation['Consumer Defensive Monthly Returns (%)'] = find_returns(consumer_list)

print(correlation.corr())


# ## Contribution Declaration
# 
# The following team members made a meaningful contribution to this assignment:
# 
# Alex Liu, Stephen Chen, Bhavya Shah
