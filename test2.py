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
string='RESTRUCTURING'
print(len(string))
soup = BeautifulSoup(string, 'html.parser')                                 #read as BeautifulSoup object
raw_text= soup.get_text(strip=True)      
print(raw_text)                               #Get raw text from filing
complete_list=tokenizer.tokenize(raw_text)    
print(complete_list)                              #apply tokenizer (token defined above)
complete_list=[x.lower() for x in complete_list] 
print(complete_list)                           #set all token to lowercase
complete_list=[x for x in complete_list if d.check(x)==True]                #Check if word is in english dictionary (valid word and no html element)
print(complete_list)

