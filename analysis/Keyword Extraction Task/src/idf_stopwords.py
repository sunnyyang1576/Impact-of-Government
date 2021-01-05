
import pandas as pd
import numpy as np



idf_dict_dir = "data/user_idf_dict.txt"
cut_number = 10
output_title = "data/idf_stopwords.txt"



with open(idf_dict_dir) as f:
    
    idf_dict = f.read()
    idf_dict = idf_dict.splitlines()




word_list = []
freq_list = []
for string in idf_dict:

    try:

        word,freq = string.strip().split()
        word_list.append(word)
        freq_list.append(float(freq))
        
    except:

    	continue


df = pd.DataFrame({"word":word_list,"freq":freq_list})



df["cut"] = pd.qcut(df.freq,cut_number,labels=False,duplicates="drop")

high_DF_df = df[df.cut==0]
high_DF_word = high_DF_df.word


with open(output_title,"w+") as f:
    
    for word in high_DF_word:
        
        f.write(word+"\n")

#### The tf-idf algorithm can be revised to improve the extraction on document with different document length
#### For detilas refers to the paper Graph of word and TW-IDF

print("Success!")


