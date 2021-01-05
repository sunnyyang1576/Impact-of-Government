
import pandas as pd
import numpy as np
import jieba
from os import listdir
import re

jieba.enable_paddle()



text_dir = "data/policy_text/"
output_file = "data/user_idf_dict.txt"


policy_dir = listdir(text_dir)



text_list = []
for file in policy_dir:
    file = text_dir+file
    
    with open(file,"r+")  as f:
        text = f.read()
    
    text = re.sub("\n","",text)
    text = re.sub("\u3000","",text)
    
    text_list.append(text)


DF = {}
for text in text_list:
    
    word_list = jieba.cut(text,cut_all=False,use_paddle=False)
    word_list = set(word_list)
    
    for word in word_list:
        try:
            DF[word] = DF[word]+1
        except:
            DF[word] = 1


total_text = len(text_list)


for word in DF.keys():
    
    DF[word] = np.log(total_text/(DF[word]+1))


with open(output_file,"w+") as f:
    for word in DF.keys():
        string = word + " " + str(DF[word]) + "\n"
        f.write(string) 

print("Success.")

