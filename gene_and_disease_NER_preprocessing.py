# -*- coding: utf-8 -*-
# conda install beautifulsoup4
# conda install lxml
# conda install NLTK

# 先執行train_test_split.py，並把train_test_split.py中的datatype設定為NER，再執行本程式。
from bs4 import BeautifulSoup
import re
import nltk

# from nltk.tokenize import word_tokenize
from joblib.numpy_pickle_utils import xrange


def tokenize(sent):
    sent = nltk.word_tokenize(sent)
    return sent


def remove_items(test_list, item):
    # remove the item for all its occurrences
    for i in test_list:
        if (i == item):
            test_list.remove(i)
    return test_list


def read_file(path, skip_lines_num):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = lines[skip_lines_num:]
    return lines


def write_file(path, write_data):
    with open(path, 'w', encoding='utf-8') as writer:
        writer.writelines(write_data)


# --setup paramaters
data_name = './NER_Format/DisGeNET_rawdata/devel.tsv'
output_file_name="./devel.tsv"
process_col_number = 1  # 取第2個欄位
process_type = "disease"  # gene or disease
max_sentence_length = 100  # 最大句子長度
# ------------------

target_dict = {}
results = []
writedata = []
filter_num = 0
lines = read_file(data_name, 0)  # 讀檔不跳行
for line in lines:
    temp = line.split("\t")
    line = temp[process_col_number]
    # print(line)
    soup = BeautifulSoup(line, "lxml")
    genes = soup.find_all("span", class_="gene", id=re.compile("[A-Za-z]+"))  # read gene tag
    diseases = soup.find_all("span", class_="disease", id=re.compile("[A-Za-z]+"))  # read disease tag
    t_count = 0
    target_dict.clear()
    results.clear()
    if (process_type is "gene"):
        for gene in genes:  # 處理gene tage欄位
            if (genes != None):
                # print("GeneName: " + gene.text)
                gene_id = str(gene).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
                # print("gene_id= " + gene_id)
                line = line.replace(gene_id, "$G" + str(t_count) + "$")
                target_dict["G" + str(t_count)] = gene.text
                t_count += 1
        for disease in diseases:  # 處理disease tag欄位
            if (diseases != None):
                # print("DiseaseName: " + disease.text)
                disease_id = str(disease).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
                # print("disease_id= " + disease_id)
                line = line.replace(disease_id, disease.text)
    if (process_type is "disease"):
        for disease in diseases:  # 處理gene tage欄位
            if (disease != None):
                # print("GeneName: " + gene.text)
                disease_id = str(disease).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
                # print("gene_id= " + gene_id)
                line = line.replace(disease_id, "$D" + str(t_count) + "$")
                target_dict["D" + str(t_count)] = disease.text
                t_count += 1
        for gene in genes:  # 處理disease tag欄位
            if (genes != None):
                # print("DiseaseName: " + disease.text)
                gene_id = str(gene).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
                # print("disease_id= " + disease_id)
                line = line.replace(gene_id, gene.text)
    # print(line)
    # print(gene_dict)
    results = tokenize(line)  # 英文斷詞
    results = remove_items(results, "$")
    if len(results) > max_sentence_length:  # 如果句子長度大於max_sentence_length就pass不處理
        #print(len(results))
        filter_num = filter_num + 1
        continue
    for i in xrange(len(results)):
        dict_check = target_dict.get(results[i], "empty")
        if (dict_check != "empty"):
            temp = dict_check.split(" ")
            for j in xrange(len(temp)):
                if (j == 0):
                    writedata.append(temp[j] + "\tB" + "\n")
                else:
                    writedata.append(temp[j] + "\tI" + "\n")
        else:
            writedata.append(results[i] + "\tO" + "\n")
        # print(results[i])
    writedata.append("\n")
write_file(output_file_name, writedata)
print("The Number of Filtered Sentences =" + str(filter_num))
print("Processing Done")
