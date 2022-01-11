import settings
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_excel(settings.csv_path + '/data2.xlsx', index_col=0)
sic_list = df['sicDescription'].unique()
for i, industry in enumerate(sic_list):
    df.loc[df.sicDescription == industry, "industrynumber"] = i
df = df.drop(['change','change_abs'], axis=1)
print(df.shape)
df= df.dropna()
print(df.shape)
#fit regression model
model = LinearRegression()
X, y = df[["tone","industrynumber",'analyst','marketCap_log', 'averageVolume_log','priceToBook','doc_size_log']], df.abnormal_return
model.fit(X, y)
#'analyst','marketCap_log', 'averageVolume_log','priceToBook'
#display adjusted R-squared
print(1 - (1-model.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1))

#print(model.score(X,y))