import settings
import pandas as pd
import json
import MOD_Load_MasterDictionary_v2020 as LM

'''
Part 6

This file creates a excel file that contains a ranking for word occurrence (ranking for complete data)
'''

stopwords = ['ME', 'MY', 'MYSELF', 'WE', 'OUR', 'OURS', 'OURSELVES', 'YOU', 'YOUR', 'YOURS',
                  'YOURSELF', 'YOURSELVES', 'HE', 'HIM', 'HIS', 'HIMSELF', 'SHE', 'HER', 'HERS', 'HERSELF',
                  'IT', 'ITS', 'ITSELF', 'THEY', 'THEM', 'THEIR', 'THEIRS', 'THEMSELVES', 'WHAT', 'WHICH',
                  'WHO', 'WHOM', 'THIS', 'THAT', 'THESE', 'THOSE', 'AM', 'IS', 'ARE', 'WAS', 'WERE', 'BE',
                  'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'HAVING', 'DO', 'DOES', 'DID', 'DOING', 'AN',
                  'THE', 'AND', 'BUT', 'IF', 'OR', 'BECAUSE', 'AS', 'UNTIL', 'WHILE', 'OF', 'AT', 'BY',
                  'FOR', 'WITH', 'ABOUT', 'BETWEEN', 'INTO', 'THROUGH', 'DURING', 'BEFORE',
                  'AFTER', 'ABOVE', 'BELOW', 'TO', 'FROM', 'UP', 'DOWN', 'IN', 'OUT', 'ON', 'OFF', 'OVER',
                  'UNDER', 'AGAIN', 'FURTHER', 'THEN', 'ONCE', 'HERE', 'THERE', 'WHEN', 'WHERE', 'WHY',
                  'HOW', 'ALL', 'ANY', 'BOTH', 'EACH', 'FEW', 'MORE', 'MOST', 'OTHER', 'SOME', 'SUCH',
                  'NO', 'NOR', 'NOT', 'ONLY', 'OWN', 'SAME', 'SO', 'THAN', 'TOO', 'VERY', 'CAN',
                  'JUST', 'SHOULD', 'NOW', 'AMONG']

MASTER_DICTIONARY_FILE = 'LoughranMcDonald_MasterDictionary_2020.csv'
lm_dictionary = LM.load_masterdictionary(
    MASTER_DICTIONARY_FILE, print_flag=True)
df = pd.read_excel(settings.csv_path + '/return_result.xlsx', index_col=0)

counter_dict = {}
counter = 0
for file in df['token']:  # iterate tokens of 10-K
    counter += 1
    with open(settings.tenk_path + '/' + file.split('/')[-2] + '/' + file.split('/')[-1], 'r') as f:
        temp_list = json.load(f)
    for x in temp_list:  # Create dict for word count
        if x not in counter_dict:
            counter_dict[x] = 1
        else:
            counter_dict[x] += 1
    print(counter)


df1 = pd.DataFrame.from_dict(
    counter_dict,
    orient='index',
    columns=['word'])  # No filter
df1 = df1.sort_values(by='word', ascending=False)

# filter dicts

counter_stop = counter_dict.copy()  # Stop words

for word in stopwords:
    if word in counter_stop:
        del counter_stop[word]

df2 = pd.DataFrame.from_dict(counter_stop, orient='index', columns=['word'])
df2 = df2.sort_values(by='word', ascending=False)

counter_neg = counter_dict.copy()  # Neg

for key in list(counter_neg):
    try:
        if not lm_dictionary[key.upper()].negative:
            del counter_neg[key]
    except BaseException:
        del counter_neg[key]

df3 = pd.DataFrame.from_dict(counter_neg, orient='index', columns=['word'])
df3 = df3.sort_values(by='word', ascending=False)
counter_pos = counter_dict.copy()  # Pos

for key in list(counter_pos):
    try:
        if not lm_dictionary[key.upper()].positive:
            del counter_pos[key]
    except BaseException:
        del counter_pos[key]

df4 = pd.DataFrame.from_dict(counter_pos, orient='index', columns=['word'])
df4 = df4.sort_values(by='word', ascending=False)
counter_unc = counter_dict.copy()  # Unc

for key in list(counter_unc):
    try:
        if not lm_dictionary[key.upper()].uncertainty:
            del counter_unc[key]
    except BaseException:
        del counter_unc[key]

df5 = pd.DataFrame.from_dict(counter_unc, orient='index', columns=['word'])
df5 = df5.sort_values(by='word', ascending=False)

with pd.ExcelWriter(settings.csv_path + '/text_statistic.xlsx') as writer:

    df1.to_excel(writer, sheet_name="No filter")
    df2.to_excel(writer, sheet_name="No stop words")
    df3.to_excel(writer, sheet_name="Only negative")
    df4.to_excel(writer, sheet_name="Only positive")
    df5.to_excel(writer, sheet_name="Only uncertainty")

    writer.save()
