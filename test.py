from os import error
import settings
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score



#speech_lenght_log
#industry
#priceToBook
#numberOfAnalystOpinions

if __name__ == '__main__':
    df = pd.read_excel(settings.csv_path + '/data.xlsx', index_col=0)
    df_check=df.loc[df['column_name'] == np.nan]
    tickers = df_check['ticker'].unique() 
    counter = 0
    for ticker in tickers:
        counter+=1
        tick = yf.Ticker(ticker)
        info = tick.info
        try:
            df.loc[df.ticker == ticker, "doc_size_log"] = np.log(df['number of words'])
            df.loc[df.ticker == ticker, "averageVolume_log"] = np.log(info['averageVolume'])
            df.loc[df.ticker == ticker, "marketCap_log"] = np.log(info['marketCap'])
            df.loc[df.ticker == ticker, "institutions"] = info['heldPercentInstitutions']
            df.loc[df.ticker == ticker, "analyst"] = info['numberOfAnalystOpinions']
            df.loc[df.ticker == ticker, "priceToBook"] = info['priceToBook']
            df.to_excel(settings.csv_path + '/data2.xlsx')
            print(counter)
        except Exception as e:
            print(e)
    df.to_excel(settings.csv_path + '/data2.xlsx')




#coefficient_of_dermination = r2_score(y, p(x))