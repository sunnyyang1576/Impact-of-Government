import pandas as pd
import numpy as np
import time
from src.GWY_news_utils import (aggregate_content,calculate_attitude_score,load_dictionary)
import jieba
import os



user_defined_dictionary_directory = "dictionary/ref_dictionary/"
lexicon_directory = "dictionary/ref_dictionary/"
content_directory = "data/"
output_directory = "data/output/"


lexicon_name = "regulation_refinement.txt"
content_name = "GWY_CWHY_content.xls"
user_defined_dictionary = "user_defined_dict.txt"
output_name = "index_regulation_refinement_cwhy"


#### Import the content series ####

premier_df = pd.read_excel(content_directory+content_name) 
premier_df = premier_df.iloc[:,1:]
premier_df.index = pd.to_datetime(premier_df.date)
content = premier_df.content

#### Load in the dictionary ####

dictionary = load_dictionary(lexicon_directory+lexicon_name)


#### Aggregate the content into different frequency ####

#daily_series = aggregate_content("B",content)
weekly_series = aggregate_content("W",content)
monthly_series = aggregate_content("BM",content)


#### Import the user defined dictionary ####


jieba.load_userdict(user_defined_dictionary_directory+user_defined_dictionary)



#### Calculate the attitude score ####

m_score = calculate_attitude_score(monthly_series,dictionary)
w_score = calculate_attitude_score(weekly_series,dictionary)
#d_score = calculate_attitude_score(daily_series,dictionary)



m_score.to_csv(output_directory+output_name+"_m.csv")
w_score.to_csv(output_directory+output_name+"_w.csv")
#d_score.to_csv(output_directory+output_name+"_d.csv")




