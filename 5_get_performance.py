import yfinance as yf
import pandas as pd
import settings

'''
Part 5

This file calculates the abnormal return for all 10K filings
'''


def get_spy_data():  # Download historic SP500 data
    spy = yf.Ticker("SPXEW") #For some reason the SP500 Equal Weight is sometimes not avialable
    start = settings.start_date
    end = settings.end_date
    spy_hist = spy.history(start=start, end=end, interval='1d', progress=True)
    spy_hist.to_json(settings.json_path + '/SPY.json')


def get_prices(df_ticker, hist):
    print(df_ticker['filingDate'])
    try:  # Check if filing date appears in df
        index = hist.index.get_loc(df_ticker['filingDate'])
        index1 = SPY_df.index.get_loc(df_ticker['filingDate'])
    except KeyError:
        index = -1
        index1 = -1
        print('not found')
    try:
        if index1 > 0 and index > 0:
            prices_stock = hist.iloc[index +
                                     settings.event_start: index +
                                     settings.event_end]
            prices_spy = SPY_df.iloc[index1 +
                                     settings.event_start:index1 +
                                     settings.event_end]
            for i in range(
                    0,
                    settings.event_end -
                    settings.event_start):  # Save prices in df
                df_ticker['s' + str(i)] = prices_stock['Close'][i]
                df_ticker['i' + str(i)] = prices_spy['Close'][i]
            return df_ticker
        else:
            return df_ticker
    except BaseException:
        pass


if __name__ == '__main__':
    get_spy_data()
    SPY_df = pd.read_json(settings.json_path + '/SPY.json')
    df = pd.read_excel(settings.csv_path + '/parsingdata.xlsx', index_col=0)
    # Transform filing data in datetime object
    df['filingDate'] = pd.to_datetime(df['filingDate'])
    tickers = df['ticker'].unique()  # Get list of all company tickers

    df_list = []
    counter = 0
    for ticker in tickers:
        counter += 1
        # Get all dataframe rows for unique ticker
        df_ticker = df.loc[df['ticker'] == ticker]
        tick = yf.Ticker(ticker)
        start1 = settings.start_date
        end1 = settings.end_date
        # Get company stock data for intervall
        hist = tick.history(
            start=start1,
            end=end1,
            interval='1d',
            progress=True)
        if hist.empty:  # Skip ticker if nothing is found
            print('Nicht gefunden')
            continue
        # get_prices for all filings of one ticker
        df_ticker = df_ticker.apply(get_prices, hist=hist, axis=1)
        df_list.append(df_ticker)
        print(counter, ticker)

    final_df = pd.concat(df_list)
    print(final_df)
    final_df['abnormal_return'] = 0
    for i in range(
            0,
            settings.event_end -
            settings.event_start -
            1):  # Calculate abnormal return + update CAR
        final_df['abnormal_return' + str(i)] = ((final_df['s' + str(i + 1)] / final_df['s' + \
            str(i)]) - 1) - ((final_df['i' + str(i + 1)] / final_df['i' + str(i)]) - 1)
        final_df['abnormal_return'] = final_df['abnormal_return'] + \
            final_df['abnormal_return' + str(i)]
        final_df = final_df.drop( [ 's' + str(i), 'i' + str(i)], axis=1)  # Drop
    final_df = final_df.dropna(subset=['abnormal_return'])
    final_df = final_df.drop(['act',
                              'primaryDocDescription',
                              'fileNumber',
                              'filmNumber',
                              'size',
                              'i' + str(settings.event_end - settings.event_start - 1),
                              's' + str(settings.event_end - settings.event_start - 1)],
                             axis=1)
    final_df.to_excel(settings.csv_path + '/return_result.xlsx')
