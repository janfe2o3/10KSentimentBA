from numpy.core.fromnumeric import shape
import yfinance as yf
import pandas as pd
import datetime
import calendar
from tqdm import tqdm
from dateutil.relativedelta import relativedelta



def get_spy_data():
    spy = yf.Ticker("SPY")
    start= "2000-01-01"
    end ="2021-10-01"
    spy_hist = spy.history( start=start, end= end,interval='1d', progress=True)

    spy_hist.to_json('SPY.json')

def get_prices(df_ticker, hist):
        print(df_ticker['filingDate'])
        try:
            index = hist.index.get_loc(df_ticker['filingDate'])
        except KeyError:
            print(hist)
            index=-1
        try:
            index1 = SPY_df.index.get_loc(df_ticker['filingDate'])
        except KeyError:
            print(hist)
    
            index1=-1
        if index1>0  and index >0:
            print(index)
            prices_stock= hist.iloc[index-5:index+2]
            prices_spy = SPY_df.iloc[index1-5:index1+2]

            df_ticker['1_price_filing']=prices_stock['Close'][0]
            df_ticker['2_price_period_end']=prices_stock['Close'][-1]
            df_ticker['1_spy_price']=prices_spy['Close'][0]
            df_ticker['2_spy_price']=prices_spy['Close'][-1]
            return df_ticker

get_spy_data()
SPY_df= pd.read_json('SPY.json')
df=pd.read_csv('download_info.csv', sep=';')
df['filingDate'] = pd.to_datetime(df['filingDate'])
tickers= df['ticker'].unique()

df_list=[]
counter=0
#print(len(tickers))
for ticker in tickers:
    counter+=1
    df_ticker = df.loc[df['ticker']==ticker]
    tick = yf.Ticker(ticker)
    start1='2000-01-01'
    end1 ='2021-12-31'
    hist = tick.history( start=start1, end= end1,interval='1d', progress=True)
    if hist.empty:
        print('Nicht gefunden')
        continue
    df_ticker= df_ticker.apply(get_prices, hist=hist, axis=1)
    df_list.append(df_ticker)
    #if counter==20:
    #    break
    print(counter, ticker)

final_df= pd.concat(df_list)

final_df['percent']= (final_df['2_price_period_end']/final_df['1_price_filing'])-1
final_df['percentSPY']= (final_df['2_spy_price']/final_df['1_spy_price'])-1
final_df['abnormal_return']= final_df['percent']-final_df['percentSPY']
final_df= final_df.drop(['Unnamed: 0'],axis=1)
final_df= final_df.dropna(subset=['abnormal_return'])
final_df.to_csv('price_info.csv', sep=";", decimal=',')
print(final_df)

