from numpy.core.fromnumeric import shape
import yfinance as yf
import pandas as pd
import datetime
import calendar
from tqdm import tqdm
from dateutil.relativedelta import relativedelta

dummy_hist= pd.read_excel('dummy.xlsx')

def get_spy_data():
    spy = yf.Ticker("SPY")
    start= "2000-01-01"
    #end ="2021-10-01"
    spy_hist = spy.history( start=start,interval='1d', progress=True) #end= end,interval='1d', progress=True)

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

            for i in range(0,7):
                df_ticker['s'+str(i)]=prices_stock['Close'][i]
                df_ticker['i'+str(i)]=prices_spy['Close'][i]
            return df_ticker
        else:
            prices_stock= dummy_hist
            prices_spy = dummy_hist
            for i in range(0,7):
                df_ticker['s'+str(i)]=prices_stock['Close'][i]
                df_ticker['i'+str(i)]=prices_spy['Close'][i]
            return df_ticker
get_spy_data()
SPY_df= pd.read_json('SPY.json')
df=pd.read_csv('tokencsv1.csv', sep=';')
df['filingDate'] = pd.to_datetime(df['filingDate'], dayfirst=True)
print(df)
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
print(final_df)
final_df.to_csv('dfcsv.csv', sep=";", decimal=',')
final_df['abnormal_return1']= (final_df['s1']/final_df['s0']-1)-(final_df['i1']/final_df['i0']-1)
final_df['abnormal_return2']= (final_df['s2']/final_df['s1']-1)-(final_df['i2']/final_df['i1']-1)
final_df['abnormal_return3']= (final_df['s3']/final_df['s2']-1)-(final_df['i3']/final_df['i2']-1)
final_df['abnormal_return4']= (final_df['s4']/final_df['s3']-1)-(final_df['i4']/final_df['i3']-1)
final_df['abnormal_return5']= (final_df['s5']/final_df['s4']-1)-(final_df['i5']/final_df['i4']-1)
final_df['abnormal_return6']= (final_df['s6']/final_df['s5']-1)-(final_df['i6']/final_df['i5']-1)
#final_df['abnormal_return3']= (final_df['s3']/final_df['s2']-1)-(final_df['i3']/final_df['i2']-1)
final_df['abnormal_return']= final_df['abnormal_return1']+final_df['abnormal_return2']+final_df['abnormal_return3']+final_df['abnormal_return4']+final_df['abnormal_return5']+final_df['abnormal_return6']
final_df= final_df.drop(['Unnamed: 0'],axis=1)
final_df= final_df.dropna(subset=['abnormal_return'])
final_df.to_csv('price_info.csv', sep=";", decimal=',')
print(final_df)

