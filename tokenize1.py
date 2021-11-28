from bs4 import BeautifulSoup
import re
from numpy.core.defchararray import lower
from numpy.lib.shape_base import column_stack
import pandas as pd
from collections import Counter
import json
from nltk.tokenize import RegexpTokenizer
from bs4.element import Comment
import enchant
import os.path
from os import path
import nltk
from nltk.corpus import stopwords
import settings


stop_words = set(stopwords.words('english'))
d = enchant.Dict("en_US")

tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,12}\b')

print(type(stop_words))
df= pd.read_csv(settings.csv_path+'/download_report.csv', sep=";", index_col=0)
df['token']=''

print('shape',df.shape)
print(df)
counter=0
list1= []

for filing in df['path']:
    counter+=1
    #print('f',filing)
    if filing =='-1':
        df.loc[df.path ==filing,'token']= save_path
        print('invalid')
        continue
    folder= filing.split('.')[0]
    save_path=folder+'.json'
    if path.exists(save_path):# and save_path in df['token'].unique():
        df.loc[df.path ==filing,'token']= save_path
        print('existing')
        continue
    print(counter)
    with open(filing, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    raw_text= soup.get_text(strip=True)
    complete_list=tokenizer.tokenize(raw_text)
    complete_list=[x.lower() for x in complete_list]
    complete_list=[x for x in complete_list if d.check(x)==True]
    print(save_path)

    df.loc[df.path ==filing,'token']= save_path
    with open(save_path, 'w') as f:
        json.dump(complete_list, f, indent=4)
    if (counter % 20) == 0:
        df.to_csv(settings.csv_path+'/tokencsv.csv', sep=';')
        print('saving')
        #break

df.to_csv(settings.csv_path+'/tokencsv.csv', sep=';')
print('finished')

