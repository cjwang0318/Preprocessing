# -*- coding: utf-8 -*-

def remove_items_in_list(test_list, item):
    # remove the item in a list for all its occurrences
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
