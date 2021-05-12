# -*- coding: utf-8 -*-
# conda install beautifulsoup4
# conda install lxml
# conda install NLTK

#請先執行本程式，再去執行train_test_split.py，並把train_test_split.py中的datatype設定為RE
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
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    lines = lines[skip_lines_num:]
    return lines


def write_file(path, write_data):
    with open(path, 'w', encoding='utf-8') as writer:
        writer.writelines(write_data)


# --setup paramaters
# data_name = 'gene_evidences.tsv'
data_name = 'C:/Users/ITRI/Desktop/gene_evidences.tsv'
process_col_number = 1  # 取第2個欄位
process_type = "disease-gene"  # gene or disease
# ------------------

target_dict = {}
results = []
writedata = ["sentence\tlabel\n"]
lines = read_file(data_name, 1)  # 讀檔且第一行跳過
used_count = 0
for line in lines:
    temp = line.split("\t")
    line = temp[process_col_number]
    # print(line)
    soup = BeautifulSoup(line, "lxml")
    genes = soup.find_all("span", class_="gene", id=re.compile("[A-Za-z]+"))  # read gene tag
    diseases = soup.find_all("span", class_="disease", id=re.compile("[A-Za-z]+"))  # read disease tag
    # print("Number of genes in a sentence:"+str(len(genes)))
    # print("Number of disease in a sentence:" + str(len(diseases))+"\n")
    g_count = len(genes)
    t_count = len(diseases)
    if (g_count == 1 and t_count == 1):
        used_count += 1
        for gene in genes:  # 處理gene tag欄位
            gene_id = str(gene).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
            line = line.replace(gene_id, "@GENE$")
        for disease in diseases:  # 處理disease tag欄位
            disease_id = str(disease).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
            line = line.replace(disease_id, "@DISEASE$")
        writedata.append(line + "\t1\n")
write_file(process_type + ".txt", writedata)
print("Total selected number="+str(used_count))
print("Processing Done")
