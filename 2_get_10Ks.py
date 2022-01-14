import pandas as pd
import json
import requests
import os
from pathlib import Path
from requests.models import HTTPError
import settings
cik = __import__('1_get_cik_jsons')

"""
Part 2
This file downloads all 10ks from the submission jsons and saves the result in download_report.csv

"""

heads = {
    '''User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36''',
}


def get_files():
    paths = []
    root = settings.json_path  # Setting download path as root folder to search in
    for path, subdirs, files in os.walk(root):  
        # Iterating over all files in root
        for name in files:
            if name.endswith('.json'):
                # If file is json file add filepath to list
                paths.append(os.path.join(path, name))
    return paths


def get_filings(path):
    def download(df):
        accessionNumber = df['accessionNumber'].replace('-', '')
        primaryDocument = df['primaryDocument']
        reportDate = df['reportDate']
        down_direct = settings.tenk_path
        # Creating dwonload path for filing
        path_filing = f'{down_direct}/{ticker}/{reportDate}.htm'
        if os.path.exists(
                path_filing) == False:  # check if filing is already downloaded
            try:
                # url pattern for downloading 10ks
                url = f"https://www.sec.gov/Archives/edgar/data/{CIK}/{accessionNumber}/{primaryDocument}"
                response = requests.get(url, headers=heads)
                print(url)
                response.raise_for_status()
                Path(f"{down_direct}/{ticker}/").mkdir(parents=True, exist_ok=True)
                with open(path_filing, 'wb') as f:  # Saving filing original
                    f.write(response.content)

            except HTTPError:  # Error if filing is not existing
                print('error', path_filing)
                path_filing = -1
        df['path'] = path_filing  # Saving metadate in df
        df['ticker'] = ticker
        df['sicDescription'] = sicDescription
        df['fiscalYearEnd'] = fiscalYearEnd
        df['exchange'] = exchange
        df['name'] = name
        return df

    with open(path) as json_file:  # Load JSON-file
        data = json.load(json_file)
    try:  # Checking if for atributes. If metadata is not in JSON add error code -1 instead
        ticker = data['tickers'][0]
    except BaseException:
        ticker = -1
    try:
        exchange = data['exchanges'][0]
    except BaseException:
        exchange = -1
    try:
        fiscalYearEnd = data['fiscalYearEnd']
    except BaseException:
        fiscalYearEnd = -1
    try:
        sicDescription = data['sicDescription']
    except BaseException:
        sicDescription = -1
    try:
        name = data['name']
    except BaseException:
        name = -1
    print(data['cik'])
    CIK = cik.longCIK(data['cik'])
    # creating Dataframe for company
    df = pd.DataFrame.from_dict(data['filings']['recent'])

    df = df.loc[df['form'] == "10-K"]  # Filtering for all 10K entries
    df['json_path'] = path
    df = df.apply(download, axis=1)  # Downloading all 10Ks for CIK
    return df


if __name__ == '__main__':
    # Create path list with all downloaded JSONs from 1_get_cik_jsons.py
    path_list = get_files()
    counter = 0
    df_list = []
    for path in path_list:
        counter += 1
        # Creating DataFrame row for every company
        df_list.append(get_filings(path))
        print(counter)

    final_df = pd.concat(df_list)  # Adding filing from all companies together
    print(final_df)
    final_df.to_csv(
        settings.csv_path +
        '/download_report.csv',
        sep=";")  # CSV summary table
    print(final_df)
