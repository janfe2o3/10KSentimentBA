import pandas as pd
import settings

'''
Part 6

This file calculates the change in Tone in comparsion to the previous year
'''

df = pd.read_excel(settings.csv_path + '/return_result.xlsx', index_col=0)

tickers = df['ticker'].unique()

list1 = []
for ticker in tickers:
    df1 = df.loc[df['ticker'] == ticker]
    df1 = df1.sort_values(by='filingDate', ascending=True)
    if df1.shape[0] > 1:

        df1['change'] = df1['% negative'].diff(
        ) / df1['% negative'].abs().shift()
        df1['change_abs'] = df1['% negative'] - df1['% negative'].shift()

    list1.append(df1)

df = pd.concat(list1)
df['reportDate'] = pd.to_datetime(df['reportDate'])
df = df.loc[(df['reportDate'] > '2010-10-1') &
            (df['reportDate'] <= '2021-11-1')]

df.to_excel(settings.csv_path + '/data.xlsx')
