import pandas as pd
import settings
import os
import openpyxl
import time



df = pd.read_excel(settings.csv_path+'/return_result.xlsx', index_col=0)

tickers= df['ticker'].unique()

list1=[]
for ticker in tickers:
    df1= df.loc[df['ticker']==ticker]
    df1= df1.sort_values(by='filingDate',ascending=True)
    if df1.shape[0]>1:

        df1['change'] = df1['tone'].diff() / df1['tone'].abs().shift()
        df1['change_abs'] = df1['tone']- df1['tone'].shift()
    
    list1.append(df1)

df = pd.concat(list1)
df['reportDate'] = pd.to_datetime(df['reportDate']) 
df= df.loc[(df['reportDate'] > '2010-10-1') & (df['reportDate'] <= '2021-11-1')]

df.to_excel(settings.csv_path+'/data.xlsx')


wb = openpyxl.load_workbook(filename = settings.csv_path+'/data.xlsx')
ws = wb.worksheets[0]

for col in ['E','F','G','H','I','J','K','L','M','N','O','P','Q','S','N','O','P','T','U','V','W','X','Z','AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ','AK','AL','AP','AQ','AR','AS','AU','AV','AW','AX','AY','AZ','BA','BB','BD','BE','BF']:              #['acceptanceDateTime', 'act', 'form','fileNumber','filmNumber','items','size','isXBRL','primaryDocument','isInlineXBRL','primaryDocument','primaryDocDescription','json_path','path',
                                                                                     #'fiscalYearEnd','exchange','name','token','file size','negative','positive','uncertainty','litigious','strong modal','weak modal','constraining','# of alphabetic','# of digits',
                                                                                    # '# of numbers','avg # of syllables per word','average word length','vocabulary','% litigious','% strong modal','% weak modal','% constraining','s0','s1','s2,s3','i0','i1','i2','i3',
                                                                                    # 'abnormal_return0','abnormal_return1','abnormal_return2']:
    ws.column_dimensions[col].hidden = True


wb.save(os.path.join(settings.csv_path,'data.xlsx'))#settings.csv_path+'/data.xlsx')

wb.close()
