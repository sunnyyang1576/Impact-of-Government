
import jieba
from collections import Counter
import pandas as pd
import statsmodels.api as sm




def GWY_URL_generator(page_number):
    """
    This function is used to generate the URL for news page on GWY website.

    :param page_number: int
    :return: str

    """
    
    return "http://sousuo.gov.cn/column/19423/{}.htm?".format(str(page_number-1))



def html_generator(x):
    
    
    html_base = "http://sousuo.gov.cn/column/30562/{}.htm".format(x)
    
    return html_base



def check_occurrance(text,list_of_words):
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
    
    ratio  = occ_agg/len(word_cut) * 100

    return ratio




def premier(x):
    """
    This function is used to check whether certain URL is premier type.
    This type of url starts with "premier"

    :param x: str
    :return: boolean

    """
    
    x = str(x)
    
    return x.startswith("http://www.gov.cn/premier")






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






def load_attitude_dictionary(dictionary_directory):
    """
    This function loads in the five government attitude lexicon. The source lexicon should be saved as a text
    in the directory.

    :param dictionary_directory: str
    :return: dict(str:list(str))

    """
    
    with open(dictionary_directory+"reform.txt") as f:
        reform_list = f.readlines()
        reform_list = [word.strip() for word in reform_list]
    
    with open(dictionary_directory+"regulation.txt") as f:
        regulation_list = f.readlines()
        regulation_list = [word.strip() for word in regulation_list]
    
    with open(dictionary_directory+"market.txt") as f:
        market_list = f.readlines()
        market_list = [word.strip() for word in market_list]
    
    with open(dictionary_directory+"intervention.txt") as f:
        intervention_list = f.readlines()
        intervention_list = [word.strip() for word in intervention_list]
    
    with open(dictionary_directory+"economy.txt") as f:
        economy_list = f.readlines()
        economy_list = [word.strip() for word in economy_list]
    
    return {"reform":reform_list,
            "regulation":regulation_list,
            "market":market_list,
            "intervention":intervention_list,
            "economy":economy_list}



def load_dictionary(dictionary_directory):

    with open(dictionary_directory) as f:

        dictionary = f.readlines()
        dictionary = [word.strip() for word in dictionary]

    return dictionary






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




def regression_x_y(y,x,y_predict_lag=1,y_include_lag=1,x_include_lag=0):
    """
    This function is used to create the y and x variable for regression analysis.
    In particular, it creates lagged variables and predicting variable from the original variable.

    :param y: pd.Series
    :param x: pd.DataFrame
    :param y_predict_lag: int
    :param y_include_lag: int
    :param x_include_lag: int
    :return: tuple(pd.DataFrame,pd.Series)




    """
    
    lag_y = y.shift(y_include_lag-1)
    pre_y = y.shift(-y_predict_lag)
    lag_x = x.shift(x_include_lag)
    
    predictor_list = [x]
    
    if y_include_lag != 0:
        
        predictor_list.append(lag_y)
    
    if x_include_lag != 0:
        
        predictor_list.append(lag_x)
    
    X = pd.concat(predictor_list,axis=1)
    
    merge_df = X.merge(pre_y,how="inner",right_index=True,left_index=True)
    merge_df.dropna(inplace=True)
    
    X = merge_df.iloc[:,0:-1]
    y = merge_df.iloc[:,-1]

    X = sm.add_constant(X)
    
    
    return X,y








