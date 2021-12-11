from bs4 import BeautifulSoup
import bs4
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


d = enchant.Dict("en_US")

tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,12}\b')

df= pd.read_csv(settings.csv_path+'/download_report.csv', sep=";", index_col=0)


print('shape',df.shape)
print(df)
counter=0
list1= []

for filing in df['path']:
    counter+=1
    folder= filing.split('.')[0]
    save_path=folder+'.json'
    if path.exists(save_path) and save_path in df['token'].unique():
       print('existing')
       continue
    print(counter)

    with open(filing, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    raw_text= soup.get_text(strip=True)
    complete_list=tokenizer.tokenize(raw_text)
    print(complete_list)
    if counter==3: break