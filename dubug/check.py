import tool_box
import os
from joblib.numpy_pickle_utils import xrange

groundtruth_file = "../test.tsv"
predict_file = "./NER_result_conll.txt"
groundtruth=tool_box.read_file(groundtruth_file,0)
predict=tool_box.read_file(predict_file,0)
print("groundtruth lines=" + str(len(groundtruth)))
print("predict lines="+str(len(predict)))
count=1
for i in xrange(len(groundtruth)):
    g_item=groundtruth[i].split("\t")
    p_item=predict[i].split(" ")
    if g_item[0] != p_item[0]:
        print(count)
        print(groundtruth[i])
        os.system("pause")
    count=count+1