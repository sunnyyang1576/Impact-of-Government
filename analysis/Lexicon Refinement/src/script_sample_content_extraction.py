

import pandas as pd
from src.dictionary_utils import check_occurrance




dictionary_directory = "dictionary/ref_dictionary/"
content_directory = "data/"
result_directory = "result/"


dictionary_name = "economy.txt"
content_name = "content.csv"




with open(dictionary_directory+dictionary_name) as f:
    dictionary = f.readlines()
    dictionary = [word.strip() for word in dictionary]


content = pd.read_csv(content_directory+content_name).content




def func(x):
    
    try: 
        result = check_occurrance(x,dictionary,normalize=True)
    except:
        result = 0
    
    return result

score_1 = content.apply(func)


def func(x):
    
    try: 
        result = check_occurrance(x,dictionary,normalize=False)
    except:
        result = 0
    
    return result



score_2 = content.apply(func)





score_df = pd.concat([content,score_1,score_2],axis=1)



score_df.columns = ["content","ratio","count_num"]



top_10_df = score_df.sort_values("ratio",ascending=False).head(10)


top_10_df.to_excel(result_directory+"top_10_df.xls")

























