import yfinance as yf
import pandas as pd
import settings

'''
Part 5

This file calculates the abnormal return for all 10K filings
'''



spy = yf.Ticker("SPY")
start= settings.start_date
end =settings.end_date
spy_hist = spy.history( start=start, end= end,interval='1d', progress=True)
spy_hist.to_json(settings.json_path+'/SPY.json')