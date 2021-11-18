import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from tqdm import tqdm
data={}
df= pd.read_csv('vektors5.csv', sep=';')
df3= pd.read_csv('tokencsv.csv', sep=";")
df3= df3.drop(['Unnamed: 0'], axis=1)
df=df.set_index(df3['accessionNumber'])
df=df.transpose()
#df1=pd.read_csv('tokencsv.csv', sep=';', decimal=',')
df2=pd.read_csv('price_info.csv', sep=';', decimal=',')
df2= df2.dropna(subset=['abnormal_return'])
df= df.drop(['Unnamed: 0'], axis=0)
x_data=[]
y_data=[]
counter_pos=0
counter_neg=0
#print(df.transpose())
for col in tqdm(df.columns):
    vector=df[col].to_numpy()
    vector= normalize(vector[:,np.newaxis], axis=0).ravel()
    try:
        performance = df2.loc[df2['accessionNumber']==col]['abnormal_return'].iloc[0]
    except:
        print('nicht gefunden')
        continue
    #print(performance)
    if np.isnan(performance):
        print(performance)
    else:
        if performance > 0:
            outperform=1
            counter_pos+=1
            x_data.append(vector)
            y_data.append(outperform)
        elif performance<0:
            outperform=0
            counter_neg+=1
            x_data.append(vector)
            y_data.append(outperform)
    
    #data[col]={}
    #data[col]['vector']=vector
    #data[col]['performance']= outperform


print('neg',counter_neg)
print('pos',counter_pos)

np.save('x_data',x_data)
np.save('y_data',y_data)


#data2=np.load('data.npy',  allow_pickle=True)


#print(data2)
print(df)