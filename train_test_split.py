from sklearn.model_selection import train_test_split

#沒有考慮label的狀態
data = [n for n in range(1, 11)]
print(data)
train_data, test_data = train_test_split(data,  train_size=0.8, random_state=777)
print(train_data)
print(test_data)