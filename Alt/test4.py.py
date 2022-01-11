from bs4 import BeautifulSoup
import pandas as pd
import json
from nltk.tokenize import RegexpTokenizer
import enchant
from os import path
import settings
from simplified_scrapy import SimplifiedDoc,req,utils

"""
Part 3
This file creates token for all 10K filings


"""

d = enchant.Dict("en_US")  # Import English dictionary
# Define Token with regular expression: -Whitespace in front and behind word
tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,20}\b')
#                                      -no numbers and only word characters
#                                      -3 to 12 characters
df = pd.read_csv(
    settings.csv_path +
    '/download_report.csv',
    sep=";",
    index_col=0)
df["filingDate"] = pd.to_datetime(df["filingDate"])
df = df.loc[(df['filingDate'] > '2010-10-1') &
            (df['filingDate'] <= '2021-10-1')]
print(len(df))
df['token'] = ''
counter = 0
list1 = []

for filing in df['path']:  # Iterating over all 10K filings
    counter += 1
    if filing == '-1':  # Check if 10K was downloaded sucessfully in previous file
        df.loc[df.path == filing, 'token'] = save_path
        print('invalid')
        continue
    folder = filing.split('.')[0]
    # Set save path for json file (contains token)
    save_path = folder + '.json'
    print(counter)
    with open(filing, encoding="utf8") as fp:
        html = req.get(fp)
        doc = SimplifiedDoc(fp)
        text = doc.body.text
        text = doc.body.unescape()
        print(text[:2000])
        
    if (counter % 1) == 0:  # save every 30 iterations
        break
        df.to_csv(settings.csv_path + '/tokencsv.csv', sep=';')
        print('saving')

# save df in csv file for next script
#df.to_csv(settings.csv_path + '/tokencsv.csv', sep=';')
print('finished')
