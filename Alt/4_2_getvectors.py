import pandas as pd
import json
from tqdm import tqdm

df= pd.read_csv('tokencsv.csv', sep=";")


with open('rank.json', 'r') as f:
    rank_dict= json.load(f)

df_list= []
header_list=[]

for header in tqdm(df['accessionNumber']):
    temp_dict= {x:0 for x in rank_dict}
    token_path= df.loc[df['accessionNumber'] == header]['token'].iloc[0]
    with open(token_path, 'r') as f:
        token_list= json.load(f)
    for i in token_list:
        if i in temp_dict:                       
            temp_dict[i]=temp_dict[i]+1
    #temp_dict= {x: temp_dict[x]/rank_dict[x] for x in temp_dict}
    #temp_dict= {x: temp_dict[x]/rank_dict[x] for x in temp_dict}
    df2 = pd.DataFrame.from_dict(temp_dict, orient='index')
    #print(df2)
    df_list.append(df2)
    header_list.append(header)


header_list= [str(x) for x in header_list]
df3= pd.concat(df_list, axis=1, keys=header_list)
#df3=df3.columns(header_list)
df3= df3.sort_index()
print(df3)
df3.to_csv('vectors3.csv', sep= ";")
