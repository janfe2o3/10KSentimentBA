import pandas as pd

def get_SP500():
    # Download list of SP500 companies from Wikipedia
    payload = pd.read_html(
        'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    first_table = payload[0]  # Current SP500
    second_table = payload[1]  # Changes in SP500
    
    return first_table, second_table


df1, df= get_SP500()
df.loc[:,'Date']=pd.to_datetime(df['Date']["Date"],format="%B %d, %Y")
df['year'] = df['Date']["Date"].dt.year

df= df.loc[(df['Date']['Date']>="2010-01-01")]

print('average changes per year:',df.groupby(df.year).agg('count')['year'].mean())

list1= df['Added']['Ticker'].to_list()
list2= df['Removed']['Ticker'].to_list()


sp= set(df1['Symbol'].to_list())

sp1=sp.copy()
print('copmpanies today:',len(sp))
for rem, add in zip(list1, list2):
    try:
        sp.remove(rem)
    except:
        pass
    try:
        sp.add(add)
    except:
        pass
    
print('copmpanies 2010:',len(sp))

counter=0
for i in sp1:
    if i in sp:
        counter+=1



print('Companies in SP500 today and 2010:',counter)
