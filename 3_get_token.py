from bs4 import BeautifulSoup
import pandas as pd
import json
from nltk.tokenize import RegexpTokenizer
import enchant
from os import path
import settings


"""
Part 3
This file creates token for all 10K filings


"""

d = enchant.Dict("en_US")                                                       #Import English dictionary
tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,12}\b')                               #Define Token with regular expression: -Whitespace in front and behind word
                                                                                #                                      -no numbers and only word characters                                            
                                                                                #                                      -3 to 12 characters
df= pd.read_csv(settings.csv_path+'/download_report.csv', sep=";", index_col=0)
df['token']=''
counter=0
list1= []

for filing in df['path']:                                                      #Iterating over all 10K filings
    counter+=1
    if filing =='-1':   	                                                   #Check if 10K was downloaded sucessfully in previous file
        df.loc[df.path ==filing,'token']= save_path
        print('invalid')
        continue
    folder= filing.split('.')[0]
    save_path=folder+'.json'                                                    #Set save path for json file (contains token)
    if path.exists(save_path):                                                  #Check if json file already exists (performance reason)
        df.loc[df.path ==filing,'token']= save_path
        print('existing')
        continue
    print(counter)
    with open(filing, encoding="utf8") as fp:                                   #read 10K filing
        soup = BeautifulSoup(fp, 'html.parser')                                 #read as BeautifulSoup object
    raw_text= soup.get_text(strip=True)                                         #Get raw text from filing
    complete_list=tokenizer.tokenize(raw_text)                                  #apply tokenizer (token defined above)
    complete_list=[x.lower() for x in complete_list]                            #set all token to lowercase
    complete_list=[x for x in complete_list if d.check(x)==True]                #Check if word is in english dictionary (valid word and no html element)
    print(save_path)

    df.loc[df.path ==filing,'token']= save_path
    with open(save_path, 'w') as f:                                             #save token list in file
        json.dump(complete_list, f, indent=4)
    if (counter % 20) == 0:                                                     #save every 20 iterations
        df.to_csv(settings.csv_path+'/tokencsv.csv', sep=';')
        print('saving')

df.to_csv(settings.csv_path+'/tokencsv.csv', sep=';')                           #save df in csv file for next script
print('finished')

