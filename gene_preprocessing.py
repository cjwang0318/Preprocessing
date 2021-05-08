# -*- coding: utf-8 -*-
# conda install beautifulsoup4
# conda install lxml
# conda install NLTK

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
    with open(path) as f:
        lines = f.readlines()
    lines = lines[skip_lines_num:]
    return lines


def write_file(path, write_data):
    with open(path, 'w') as writer:
        writer.writelines(write_data)


data_name = 'gene_evidences.tsv'
gene_dict = {}
results = []
writedata = []
lines = read_file(data_name, 1)  # 讀檔且第一行跳過
for line in lines:
    temp = line.split("\t")
    line = temp[1]  # 取第2個欄位
    # print(line)
    soup = BeautifulSoup(line, "lxml")
    genes = soup.find_all("span", class_="gene", id=re.compile("[A-Za-z]+"))  # read gene tag
    diseases = soup.find_all("span", class_="disease", id=re.compile("[A-Za-z]+"))  # read disease tag
    g_count = 0
    gene_dict.clear()
    results.clear()
    for gene in genes:  # 處理gene tage欄位
        if (genes != None):
            # print("GeneName: " + gene.text)
            gene_id = str(gene).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
            # print("gene_id= " + gene_id)
            line = line.replace(gene_id, "$G" + str(g_count) + "$")
            gene_dict["G" + str(g_count)] = gene.text
            g_count += 1
    for disease in diseases:  # 處理disease tag欄位
        if (diseases != None):
            # print("DiseaseName: " + disease.text)
            disease_id = str(disease).replace(chr(34), chr(39))  # 將雙引號轉換成單引號
            # print("disease_id= " + disease_id)
            line = line.replace(disease_id, disease.text)
    # print(line)
    # print(gene_dict)
    results = tokenize(line) #英文斷詞
    remove_items(results, "$")
    for i in xrange(len(results)):
        dict_check = gene_dict.get(results[i], "empty")
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
write_file("test.txt", writedata)
print("Processing Done")