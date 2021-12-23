stopwords=['ME', 'MY', 'MYSELF', 'WE', 'OUR', 'OURS', 'OURSELVES', 'YOU', 'YOUR', 'YOURS',
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
stopwords=[x.lower() for x in stopwords]


from nltk.tokenize import RegexpTokenizer
import MOD_Load_MasterDictionary_v2020 as LM
text1= "We rely on third parties and if they are unable to do so, our business could be materially adversely affected"
text2="To the extent any of these third parties are unable to perform these services  we can encounter supply delays that could adversely affect our business and financial results."
list1=[text1, text2]
tokenizer = RegexpTokenizer(r'\b[^\d\W]{1,12}\b') 

MASTER_DICTIONARY_FILE = r'E:/Bachelorarbeit/input/LoughranMcDonald_MasterDictionary_2020.csv'

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)



list2=[]
for text in list1:
    positive=0
    negative=0
    complete_list=tokenizer.tokenize(text)
    complete_list=[x.lower() for x in complete_list]
    complete_list=[x for x in complete_list if x not in stopwords]
    complete_list=[x.upper() for x in complete_list]
    list2+=complete_list
    print(len(complete_list))
    print(complete_list)
    for token in complete_list:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:       #Check if token is in dictionary
                                         #Raise counter by one if word fit in category
            if lm_dictionary[token].negative: 
                negative += 1    
                print(token)                   #Negative
            if lm_dictionary[token].positive: 
                positive += 1
                print(token)
    print('positive', positive)
    print('negative', negative)  

list2=set(list2)

print(len(list2))