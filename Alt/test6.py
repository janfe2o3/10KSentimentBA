from sklearn.linear_model import LinearRegression
import pandas as pd


data= pd.read_excel('C:/Users/janro/OneDrive - Universität Bayreuth/5u6Semester/Bachelorarbeit/data_re.xlsx', index_col=0)
data=data[['filingDate', 'reportDate', 'tone','abnormal_return', 'change', '% negative', 'change_abs','number of words'] ]

#fit regression model
model = LinearRegression()
X = data.loc[:, 'abnormal_return', 'number of words'].values.reshape(-1, 1)  # iloc[:, 1] is the column of X
y = data.loc[:, 'tone'].values.reshape(-1, 1)  # df.iloc[:, 4] is the column of Y
model.fit(X, y)

#display adjusted R-squared
print(1 - (1-model.score(X, y))*(len(y)-1)/(len(y)-X.shape[1]-1))