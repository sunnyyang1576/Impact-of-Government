
import os
import re
import numpy as np



directory = "data/policy_text/"
file_list = os.listdir("data/policy_text")



total_sentence_list = []

for file in file_list:
    
    file_directory = directory+file
    
    with open(file_directory) as f:
        
        sentence_list = f.readlines()
        sentence_list = [sent.strip() for sent in sentence_list]
        sentence_list = [sent for sent in sentence_list if sent != ""]
        
        total_sentence_list += sentence_list





total_sentence_list = []

for file in file_list:
    
    file_directory = directory+file
    
    with open(file_directory) as f:
        
        text = f.read()
        sentence_list = re.split("。|！|；",text)
        
        sentence_list = [sent.strip() for sent in sentence_list]
        sentence_list = [sent for sent in sentence_list if sent != ""]
        sentence_list = [sent for sent in sentence_list if sent != ""]
        
        
        total_sentence_list += sentence_list




random_index = np.random.randint(0,len(total_sentence_list),100)
random_sample = [total_sentence_list[index] for index in random_index]




with open("random_sample_sentence.txt","w+") as f:
    
    for sent in random_sample:
        sent = sent+"\n"+"\n"
        f.write(sent)



        









