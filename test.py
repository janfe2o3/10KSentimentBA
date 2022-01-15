from scipy import stats
import pandas as pd

df= pd.read_excel('C:/Users/janro/OneDrive - Universität Bayreuth/5u6Semester/Bachelorarbeit/data_re.xlsx', index_col=0)

df1= df.loc[df['tone']>df['tone'].quantile(0.5)]
df2= df.loc[df['tone']<df['tone'].quantile(0.5)]

print(df1.shape)
print(df2.shape)


x=stats.ttest_ind(df1['tone'], df2['tone'])

print(x)