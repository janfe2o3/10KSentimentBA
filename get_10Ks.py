import pandas as pd
import json
import requests
import os
from pathlib import Path
from requests.models import HTTPError
import locations
from get_cik_jsons import longCIK

"""This script downloads all 10ks from the submission jsons and saves the result in download_report.csv"""

heads = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }


def get_files():
    paths=[]
    root = locations.json_path                        #Setting download path as root folder to search in
    for path, subdirs, files in os.walk(root):              #Iterating over all files in root
        for name in files:
            if name.endswith('.json'):                      
                paths.append(os.path.join(path, name))      #If file is json file add filepath to list
    return paths


def get_filings(path):
    def download(df):
        accessionNumber = df['accessionNumber'].replace('-','')
        primaryDocument = df['primaryDocument']
        reportDate=df['reportDate']
        down_direct = locations.tenk_path
        path_filing=f'{down_direct}/{ticker}/{reportDate}.htm'         #Creating dwonload path for filing
        if os.path.exists(path_filing) == False:                       #check if filing is already downloaded
            try:
                url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/{primaryDocument}"              #url pattern for downloading 10ks
                response = requests.get(url, headers=heads)
                print(url)
                response.raise_for_status()
                Path(f"{down_direct}/{ticker}/").mkdir(parents=True, exist_ok=True)
                with open(path_filing, 'wb') as f:                      #Saving filing
                    f.write(response.content)
            except HTTPError:                                          #Error if filing is not existing
                print('error',path_filing)
                path_filing=-1
        df['path']=path_filing                                         #Saving metadate in df  
        df['ticker']= ticker
        df['sicDescription']= sicDescription
        df['fiscalYearEnd']=fiscalYearEnd
        df['exchange']=exchange
        df['name']=name
        return df

    with open(path) as json_file:                   #Load JSON-file 
        data = json.load(json_file)
    try:                                            #Checking if for atributes. If metadata is not in JSON add error code -1 instead
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
    df = pd.DataFrame.from_dict(data['filings']['recent'])          #creating Dataframe for company

    df= df.loc[df['form'] == "10-K"]                                #Filtering for all 10K entries
    df['json_path']=path                                            
    df= df.apply(download, axis=1)                                  #Downloading all 10Ks for CIK
    return df

if __name__ == '__main__':
    path_list= get_files()                      #Create path list with all downloaded JSONs from 1_get_cik_jsons.py
    counter= 0
    df_list=[]
    for path in path_list:
        counter+=1
        df_list.append(get_filings(path))      #Creating DataFrame row for every company

        print(counter)
        #if counter==5:
        #    break

    final_df= pd.concat(df_list)                            #Adding filing from all companies together
    print(final_df)
    final_df =pd.read_csv(locations.csv_path+'/download_report.csv', sep=";")
    print(final_df)