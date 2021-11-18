import pandas as pd
import requests
import os.path
from os import path


heads = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
         }
def download(CIK):
        url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
        response = requests.get(url, headers=heads)
        print(url)
        response.raise_for_status()
        download_path = r"C:/Users/janro/Uni/SEC/JSONs"

        with open(f'{download_path}/{CIK}.json', 'wb') as f:
            f.write(response.content)

def longCIK(CIK):
    CIK=str(CIK)
    while len(CIK)<10:
        CIK="0"+CIK
    return CIK

def get_SP500():
    payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]        #Current SP500
    second_table = payload[1]       #Changes in SP500
    first_table['CIK']= first_table['CIK'].apply(longCIK)
    first_table.to_csv('SP500-Aktien.csv', sep=";")
    return first_table


if path.exists('SP500-Aktien.csv'):
    df_SP=pd.read_csv('SP500-Aktien.csv', sep=";")
else:
    df_SP= get_SP500()

for i in df_SP['CIK']:                              
    CIK= str(longCIK(i))
    download(CIK)