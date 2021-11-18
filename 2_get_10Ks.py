import pandas as pd
import json
import requests
import os
from pathlib import Path

from requests.models import HTTPError


heads = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }
def get_files():
    paths=[]
    root = "C:/Users/janro/Uni/SEC/JSONs"
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.endswith('.json'):
                paths.append(os.path.join(path, name))
    return paths

def longCIK(CIK):
    CIK=str(CIK)
    while len(CIK)<10:
        CIK="0"+CIK
    CIK = str(CIK)
    return CIK


def get_filings(path):
    def download(df):
        #print(df)
        accessionNumber = df['accessionNumber'].replace('-','')
        primaryDocument = df['primaryDocument']
        reportDate=df['reportDate']
        down_direct = r"C:/Users/janro/Uni/SEC/filings"
        path_filing=f'{down_direct}/{ticker}/{reportDate}.htm'
        if os.path.exists(path_filing) == False:
            try:
                url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/{primaryDocument}"
                response = requests.get(url, headers=heads)
                print(url)
                response.raise_for_status()
                Path(f"{down_direct}/{ticker}/").mkdir(parents=True, exist_ok=True)
            
                with open(path_filing, 'wb') as f:
                    f.write(response.content)
            except HTTPError:
                print('error',path_filing)
                path_filing=-1
        df['path']=path_filing
        df['ticker']= ticker
        df['sicDescription']= sicDescription
        df['fiscalYearEnd']=fiscalYearEnd
        df['exchange']=exchange
        df['name']=name
        return df

    with open(path) as json_file:
        data = json.load(json_file)
    try:
        ticker = data['tickers'][0]    
    except:
        ticker=-1
    try:
        exchange=data['exchanges'][0]
    except:
        exchange=-1
    try:
        fiscalYearEnd=data['fiscalYearEnd']
    except:
        fiscalYearEnd=-1
    try:
        sicDescription=data['sicDescription']
    except:
        sicDescription=-1
    try:
        name=data['name']
    except:
        name=-1
    CIK= longCIK(data['cik'])
    df = pd.DataFrame.from_dict(data['filings']['recent'])

    df= df.loc[df['form'] == "10-K"]
    df['json_path']=path
    df= df.apply(download, axis=1)
    #print(df)
    return df


path_list= get_files()
counter= 0
#df=pd.DataFrame
df_list=[]
for path in path_list:
    counter+=1
    df_list.append(get_filings(path))

    print(counter)
    if counter==5:
       break

final_df= pd.concat(df_list)
print(final_df)
#final_df.to_csv('download_info.csv', sep=";")
final_df =pd.read_csv('download_info.csv', sep=";")
print(final_df)