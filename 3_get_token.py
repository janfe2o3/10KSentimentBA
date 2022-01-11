import pandas as pd
import json
from nltk.tokenize import RegexpTokenizer
from os import path
import settings
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


"""
Part 3
This file creates token for all 10K filings


"""
# Define Token with regular expression: -Whitespace in front and behind word
#                                      -no numbers and only word characters
#                                      -3 to 20 characters
tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,24}\b')
df = pd.read_csv(
    settings.csv_path +
    '/download_report.csv',
    sep=";",
    index_col=0)
LMdict = set(pd.read_csv('LoughranMcDonald_MasterDictionary_2020.csv')[
             'Word'].to_list())
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
    if path.exists(
            save_path):  # Check if json file already exists (performance reason)
        df.loc[df.path == filing, 'token'] = save_path
        print('existing')
        continue
    print(counter)
    driver = webdriver.Firefox()  # Firefox & geckodriver instalation required
    driver.get('file://' + filing)  # Load orginal 10K
    raw_text = driver.find_element_by_tag_name('body').text  # Get visible text
    driver.close()
    # apply tokenizer (token defined above)
    complete_list = tokenizer.tokenize(raw_text)
    # set all token to lowercase
    complete_list = [x.upper() for x in complete_list]
    # Check if word is in LM dictionary (valid word and no html element)
    complete_list = [x for x in complete_list if x in LMdict]
    print(save_path)
    df.loc[df.path == filing, 'token'] = save_path
    with open(save_path, 'w') as f:  # save token list in file
        json.dump(complete_list, f, indent=4)
    if (counter % 30) == 0:  # save every 30 iterations
        df.to_csv(settings.csv_path + '/tokencsv.csv', sep=';')
        print('saving')

# save df in csv file for next script
df.to_csv(settings.csv_path + '/tokencsv.csv', sep=';')
print('finished')
