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


stop_words = set(stopwords.words('english'))


d = enchant.Dict("en_US")

tokenizer = RegexpTokenizer(r'\b[^\d\W]{3,12}\b')


#with open('stop_words.json', 'r') as f:
#    stop_words= json.load(f)
#stop_words= {x for x in stop_words}

print(type(stop_words))
#df= pd.read_csv('tokencsv.csv', sep=";")
df= pd.read_csv('tokencsv1.csv', sep=";")

#df =  df[df['percent'].notna()]

#df= df[df['reportDate']> "2010-01-01"]

print('shape',df.shape)
counter=0
list1= []

for path1 in df['path']:
    counter+=1
    folder= path1.split('.')[0]
    save_path=folder+'.json'
    if path.exists(save_path) and save_path in df['token'].unique():
       print('existing')
       continue
    print(counter)
    with open(path1, encoding="utf8") as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    raw_text= soup.get_text(strip=True)
    complete_list=tokenizer.tokenize(raw_text)
    complete_list=[x.lower() for x in complete_list]
    complete_list=[x for x in complete_list if x not in stop_words]
    complete_list=[x for x in complete_list if d.check(x)==True]
    print(save_path)

    df.loc[df.path ==path1,'token']= save_path
    with open(save_path, 'w') as f:
        json.dump(complete_list, f, indent=4)
    if (counter % 20) == 0:
        df.to_csv('tokencsv1.csv', sep=';')
        print('saving')
        #break

df.to_csv('tokencsv1.csv', sep=';')
print('finished')


#print(stop_words)
