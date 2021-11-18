from matplotlib.pyplot import xlabel
import pandas as pd
import json
from tqdm import tqdm

df= pd.read_csv('tokencsv.csv', sep=";")

word_list=[]

for token_path in tqdm(df['token']):
    with open(token_path, 'r') as f:
        temp_list= json.load(f)
    word_list= list(set(temp_list+word_list))

rank_dict= {x:0 for x in word_list}

for token_path in tqdm(df['token']):
    with open(token_path, 'r') as f:
        temp_list= json.load(f)
    for x in temp_list:
        if x in rank_dict:
            rank_dict[x]=rank_dict[x]+1

for k, v in list(rank_dict.items()):
    if v < 30:
        del rank_dict[k]  
    

print(len(word_list))

with open('wordlist.json', 'w') as f:
    json.dump(word_list, f, indent=4)
with open('rank.json', 'w') as f:
    json.dump(rank_dict, f, indent=4)


