# -*- coding: utf-8 -*-
from joblib.numpy_pickle_utils import xrange
import tool_box
import pandas as pd

# --setup parameters
boshiamy_file_name = './dictionary/Basic.txt'
data_path = './data/'
result_path = "./result/"
data_list = ['train.txt', 'dev.txt', 'test.txt']
# data_list = ['dev.txt']
oov_set = set()  # define a empty set
code_dict = {}


def load_dict_data():
    file_data = tool_box.read_file(boshiamy_file_name, 0)  # load boshiamy table data
    for i in xrange(len(file_data)):
        item = file_data[i].split("\t")
        # print(item[1])
        code_dict[item[1]] = item[0]
    return code_dict


def search_character_code(word):
    code = code_dict.get(word)
    return code


def word_check(word):
    result = search_character_code(word)
    if result == None:
        oov_set.add(word)


def oov_check(word_list):
    for word in word_list:
        word_check(word)


def crf_format_output(df, empty_line_num):
    writedata = []
    df_list = df.values.tolist()
    for i in xrange(len(df_list)):
        j = 1
        # print(df_list[i])
        if i in empty_line_num:
            # print(i)
            writedata.append("\n")
        for item in df_list[i]:
            num_item_element = len(df_list[i])
            if j == num_item_element:
                writedata.append(item + "\n")
            else:
                writedata.append(item + "\t")
                j = j + 1
    return writedata


def empty_line_num_Correction(list):
    m = 0
    for n in xrange(len(list)):
        list[n] = list[n] - m
        m = m + 1


load_dict_data()  # load 無瞎米字表

# print(search_character_code("吡"))
# print(search_character_code("范"))

for file_name in data_list:
    print("Processing: " + file_name)
    datafram = pd.read_csv(data_path + file_name, sep=' ', names=["word", "Label"],
                           skip_blank_lines=False)  # 讀取csv檔，並給定属性
    datafram.insert(1, 'code_1', '#')
    datafram.insert(2, 'code_2', '#')
    datafram.insert(3, 'code_3', '#')
    datafram.insert(4, 'code_4', '#')

    empty_line_num = list(datafram.loc[pd.isna(datafram["word"]), :].index)
    empty_line_num_Correction(empty_line_num)
    # print(empty_line_num)
    datafram = datafram[datafram['word'].notna()]
    datafram = datafram.reset_index(drop=True)  # 重制index由0開始
    word_list = datafram["word"]
    # check has oov coed not in boshiamy wordlist
    # oov_check(word_list)
    # oov_df = pd.DataFrame(oov_set)
    # oov_df.rename(columns={0: 'oov'}, inplace=True)
    # oov_df.sort_values(by=['oov'], inplace=True)
    # oov_df.to_csv(result_path + "oov.txt", sep='\t', index=0, header=0)
    # print(oov_df)
    i = 0
    for word in word_list:
        code = search_character_code(word)
        # print(word+", "+ str(code))
        if code == None:
            i = i + 1
            continue
        else:
            char_list = list(code)
            j = 1
            for char in char_list:
                if (j < 5):
                    datafram.at[i, 'code_' + str(j)] = char
                    j = j + 1
                else:
                    print("This word code is over 4 character: " + word + ": " + code)
        i = i + 1
    # print(datafram)
    crf_format_data = crf_format_output(datafram, empty_line_num)
    tool_box.write_file(result_path + "crf_" + file_name, crf_format_data)

# print(word_check("////"))
# sorted(oov_set)
