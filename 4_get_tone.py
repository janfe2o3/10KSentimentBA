import sys
import datetime as dt
import MOD_Load_MasterDictionary_v2020 as LM
import settings
import pandas as pd
import json
"""
Part 4

This file calculates the Tone for all 10K filings. In addition the script calculates additional information (See OUTPUT_FIELDS)

This is a modified version of Generic_Parser.py from https://sraf.nd.edu/textual-analysis/code/ by Tim Loughran and Bill McDonald


"""

# User defined directory for files to be parsed
TARGET_FILES = settings.tenk_path + '/*.*'
# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE = '/LoughranMcDonald_MasterDictionary_2020.csv'
# User defined output file
OUTPUT_FILE = settings.csv_path + '/Parser.csv'
# Setup output
OUTPUT_FIELDS = [
    'token',
    'file size',
    'number of words',
    'negative',
    'positive',
    'uncertainty',
    'litigious',
    'strong modal',
    'weak modal',
    'constraining',
    '% negative',
    '% positive',
    '% uncertainty',
    '% litigious',
    '% strong modal',
    '% weak modal',
    '% constraining']  # Dataframe header

# Load the dictionary from  LoughranMcDonald_MasterDictionary_XXXX.csv
lm_dictionary = LM.load_masterdictionary(
    MASTER_DICTIONARY_FILE, print_flag=True)


def main():
    df2 = pd.DataFrame(columns=OUTPUT_FIELDS)
    n_files = 0
    e_count = 0
    for file in file_list:
        n_files += 1
        print(f'{n_files:,} : {file}')
        try:
            with open(file, 'r') as f:  # save token list in file
                doc = json.load(f)
        except BaseException:
            e_count += 1
            continue
        output_data = get_data(doc)
        output_data[0] = file
        output_data[1] = len(doc)
        df_length = len(df2)
        df2.loc[df_length] = output_data

    print('Errors:', e_count)
    return df2


def get_data(doc):
    vdictionary = dict()
    _odata = [0] * 10
    total_syllables = 0
    word_length = 0

    for token in doc:
        if not token.isdigit() and len(
                token) > 1 and token in lm_dictionary:  # Check if token is in dictionary
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                # Raise counter by one if word fit in category
                vdictionary[token] = 1
            if lm_dictionary[token].negative:
                _odata[3] += 1  # Negative
            if lm_dictionary[token].positive:
                _odata[4] += 1  # Positive
            if lm_dictionary[token].uncertainty:
                _odata[5] += 1
            if lm_dictionary[token].litigious:
                _odata[6] += 1
            if lm_dictionary[token].strong_modal:
                _odata[7] += 1
            if lm_dictionary[token].weak_modal:
                _odata[8] += 1
            if lm_dictionary[token].constraining:
                _odata[9] += 1
            total_syllables += lm_dictionary[token].syllables

    # Convert counts to %
    for i in range(3, 10):
        _odata.append((_odata[i] / _odata[2]) * 100)

    return _odata


if __name__ == '__main__':
    df1 = pd.read_csv(
        settings.csv_path +
        '/tokencsv.csv',
        sep=";",
        index_col=0)  # import filepaths
    file_list = df1['token'].to_list()
    start = dt.datetime.now()
    print(f'\n\n{start.strftime("%c")}\nPROGRAM NAME: {sys.argv[0]}\n')
    df2 = main()
    result = pd.merge(df1, df2, on=['token'])  # merge both dataFrame togehter
    # Calculate Tone based on positive and negative word count
    result['tone'] = (result['positive'] - result['negative']) / \
        (result['negative'] + result['positive'])
    result = result.drop(
        ['file size', 'items', 'isXBRL', 'isInlineXBRL'], axis=1)
    result.to_excel(
        settings.csv_path +
        '/parsingdata.xlsx')  # save result DataFrame
    print(f'\n\nRuntime: {(dt.datetime.now()-start)}')
    print(f'\nNormal termination.\n{dt.datetime.now().strftime("%c")}\n')
