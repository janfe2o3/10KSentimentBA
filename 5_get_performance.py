import yfinance as yf
import pandas as pd
import settings

'''
Part 5

This file calculates the abnormal return for all 10K filings
'''



def get_spy_data():                                 #Download historic SP500 data
    spy = yf.Ticker("SPY")
    start= settings.start_date
    end =settings.end_date
    spy_hist = spy.history( start=start, end= end,interval='1d', progress=True)
    spy_hist.to_json(settings.json_path+'/SPY.json')

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
        try:
            if index1>0  and index >0:
                print(index)
                prices_stock= hist.iloc[index+settings.event_start: index + settings.event_end]
                prices_spy = SPY_df.iloc[index1+settings.event_start:index1+settings.event_end]
                for i in range(0,settings.event_end-settings.event_start):
                    df_ticker['s'+str(i)]=prices_stock['Close'][i]
                    df_ticker['i'+str(i)]=prices_spy['Close'][i]
                return df_ticker
            else:
                return df_ticker
        except:
            pass

if __name__ == '__main__':
    get_spy_data()
    SPY_df= pd.read_json(settings.json_path+'/SPY.json')
    df=pd.read_excel(settings.csv_path+'/parsingdata.xlsx', index_col=0)
    df['filingDate'] = pd.to_datetime(df['filingDate'])                         #Transform filing data in datetime object
    tickers= df['ticker'].unique()                                              #Get list of all company tickers

    df_list=[]
    counter=0
    #print(len(tickers))
    for ticker in tickers:
        counter+=1
        df_ticker = df.loc[df['ticker']==ticker]                               #Get all dataframe rows for unique ticker
        tick = yf.Ticker(ticker)
        start1=settings.start_date
        end1 =settings.end_date
        hist = tick.history( start=start1, end= end1,interval='1d', progress=True)  #Get company stock data for intervall
        if hist.empty:                                                              #Skip ticker if nothing is found
            print('Nicht gefunden')
            continue
        df_ticker= df_ticker.apply(get_prices, hist=hist, axis=1)
        df_list.append(df_ticker)
        #if counter==20:
        #    break
        print(counter, ticker)

    final_df= pd.concat(df_list)
    print(final_df)
    final_df['abnormal_return']=0
    for i in range(0,settings.event_end-settings.event_start-1):
        final_df['abnormal_return'+str(i)]= (final_df['s'+str(i+1)]/final_df['s'+str(i)]-1)-(final_df['i'+str(i+1)]/final_df['i'+str(i)]-1)
        final_df['abnormal_return']=final_df['abnormal_return']+final_df['abnormal_return'+str(i)]
    final_df= final_df.dropna(subset=['abnormal_return'])
    final_df.to_excel(settings.csv_path+'/return_result.xlsx')

