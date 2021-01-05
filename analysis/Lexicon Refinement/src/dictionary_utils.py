
import jieba
from collections import Counter
import pandas as pd
import statsmodels.api as sm


def check_occurrance(text,list_of_words,normalize=True):
    """
    This function counts the number of occurances of each word in the list of words within the text.
    It then aggreagte the occurance and outputs a ratio.

    :param text: str
    :param list_of_words: list(str)
    :return: float

    """
    
    
    word_cut = list(jieba.cut(text,cut_all=True,use_paddle=True))
    
    counter = Counter(word_cut)
    
    occ_agg = 0
    
    for word in list_of_words:
        
        occ_agg += counter[word]
    
    if len(word_cut) == 0:
        
        return 0

    if normalize:
        ratio  = occ_agg/len(word_cut) * 100
        return ratio
    else:
        return occ_agg





def aggregate_content(freq,content_series):
    """

    This function is used to aggregate multiple policy/news based on the publishing date.
    It could aggregate based on daily, weekly or monthly frequency.


    :param freq: str (e.g. "B","W","BM")
    :param content_series: pd.Series(str)
    :return: pd.Series(str)

    """
    
    
    def func(x):
        
        
        total_string = ""
        
        try:
            
            for string in x:
                
                if not isinstance(string,str):
                    
                    continue
                
                total_string += string
                
        except:

            print("Error.")
        
        return total_string
        
        
    aggregate_series = content_series.resample(freq,label="right",closed="right").apply(func)
    
    return aggregate_series





def calculate_attitude_score(content_series,dict_list):
    """
    This function calculates the attitude score of each content in the series of content.
    The attitude score is based on counting the number of occurance of the words in the dict_list.

    :param content_series: pd.Series(str)
    :param dict_list: 
    :return: pd.Series(float)

    """

    
    def func(x):
        
        try: 
            
            score = check_occurrance(x,dict_list)
        
        except:
            
            score = 100
        
        return score
    
    score_list = content_series.apply(func)
    
    return score_list       







