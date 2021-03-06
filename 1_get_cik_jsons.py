import pandas as pd
import requests
from os import path, makedirs
import settings

"""
Part 1
This file gets a list of all current SP500 companies and downloads the submission history for all companies

"""

heads = {
    '''User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)
     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36''',
}


def download(CIK):      # SEC stores one JSONs for all company submissions
    url = f"https://data.sec.gov/submissions/CIK{CIK}.json"
    response = requests.get(url, headers=heads)
    print(url)
    response.raise_for_status()
    with open(f'{settings.json_path}/{CIK}.json', 'wb') as f:  # Store Json at download path
        f.write(response.content)


def longCIK(CIK):  # Ensure CIK number has 10 digits
    CIK = str(CIK)
    while len(CIK) < 10:
        CIK = "0" + CIK
    return CIK


def get_SP500():
    # Download list of SP500 companies from Wikipedia
    payload = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]  # Current SP500
    first_table['CIK'] = first_table['CIK'].apply(longCIK)
    if path.exists(settings.csv_path) == False:
        makedirs(settings.csv_path, exist_ok=True)
    first_table.to_csv(             # Save to csv file
        settings.csv_path +
        '/SP500companies.csv',
        sep=";")
    return first_table


if __name__ == '__main__':
    # Check if a list of SP500 Companies already exists
    if path.exists(
            settings.csv_path +
            '/SP500companies.csv'):
        df_SP = pd.read_csv(
            settings.csv_path +
            '/SP500companies.csv',
            sep=";")  # Read existing file
    else:
        makedirs(settings.json_path)
        df_SP = get_SP500()  # create new file

    for i in df_SP['CIK']:  # Downloading SEC archive JSON for all CIK
        CIK = str(longCIK(i))
        download(CIK)

    print('finished')
