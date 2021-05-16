# -*- coding: utf-8 -*-
import os
import string

def remove_items_in_list(test_list, item):
    # remove the item for all its occurrences
    test_list=list(filter(lambda x: x != item, test_list))
    #print(test_list)
    return test_list


def read_file(path, skip_lines_num):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines = lines[skip_lines_num:]
    return lines


def write_file(path, write_data):
    with open(path, 'w', encoding='utf-8') as writer:
        writer.writelines(write_data)

def mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def replace_punctuation(str):
    punctuation_string = string.punctuation
    for i in punctuation_string:
        str = str.replace(i, "$"+i+"$")
    return str

#test area
#a="Type-(I) 2.48"
#print(replace_punctuation(a))
