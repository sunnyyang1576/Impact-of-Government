import pandas as pd
import numpy as np
import time
from src.GWY_news_utils import (aggregate_content,calculate_attitude_score,load_dictionary)




dictionary_directory = "data/dictionary/"
input_directory = "data/"
output_directory = "data/output/sub_class/"

dictionary_name = "simplify.txt"
output_name = "index_simplify"


premier_df = pd.read_csv(input_directory+"content.csv")
premier_df = premier_df.iloc[:,1:]
premier_df.index = pd.to_datetime(premier_df.date)
content = premier_df.content


dictionary = load_dictionary(dictionary_directory+dictionary_name)




daily_series = aggregate_content("B",content)
weekly_series = aggregate_content("W",content)
monthly_series = aggregate_content("BM",content)




m_score = calculate_attitude_score(monthly_series,dictionary)
w_score = calculate_attitude_score(weekly_series,dictionary)
d_score = calculate_attitude_score(daily_series,dictionary)



m_score.to_csv(output_directory+output_name+"_m.csv")
w_score.to_csv(output_directory+output_name+"_w.csv")
d_score.to_csv(output_directory+output_name+"_d.csv")




