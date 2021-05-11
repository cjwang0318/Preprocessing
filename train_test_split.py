from sklearn.model_selection import train_test_split
import tool_box
import pandas as pd

datatype = "RE"  # NER or RE
training_proportion = 0.8  # range=0~1
random_seed = 0  # 填1其他引數隨機陣列是一樣的;填0或不填，每次都會不一樣
data_name = 'D:/PycharmProjects/Preprocessing/disease-gene.txt'
skip_lines_num = 1  # 第一行不要讀取
# 沒有考慮label的狀態(NER使用)
if (datatype is "NER"):
    data = tool_box.read_file(data_name, skip_lines_num)
    train_data, test_data = train_test_split(data, train_size=training_proportion, random_state=random_seed)
    tool_box.write_file("train.txt", train_data)
    tool_box.write_file("test.txt", test_data)

if (datatype is "RE"):
    data = pd.read_csv(data_name, sep='\t')
    # print(data.head())
    X = data["sentence"]
    Y = data["label"]
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=training_proportion, random_state=random_seed)
    train_data = pd.concat([x_train, y_train], axis=1)
    test_data = pd.concat([x_test, y_test], axis=1)
    train_data.to_csv("train.txt", sep='\t', index=0, header=0)  # 不保存列名, 不保存行索引
    test_data.to_csv("test.txt", sep='\t', index=0, header=0)  # 不保存列名, 不保存行索引
