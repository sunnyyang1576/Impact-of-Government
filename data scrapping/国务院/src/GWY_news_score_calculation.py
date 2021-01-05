
import pandas as pd
import numpy as np
import time
from GWY_news_utils import aggregate_content,calculate_attitude_score



dictionary_directory = "data/dictionary/"
output_directory = "data/output/"
result_directory = "result/"


premier_df = pd.read_csv("data/content.csv")
premier_df = premier_df.iloc[:,1:]
premier_df.index = pd.to_datetime(premier_df.date)
content = premier_df.content



### Aggregate the string into timely observation ###

daily_series = aggregate_content("B",content)
weekly_series = aggregate_content("W",content)
monthly_series = aggregate_content("BM",content)




### Import Government Attitude Dictionary ###


attitude_word_dict = load_attitude_dictionary(dictionary_directory)

reform_list = attitude_word_dict["reform"]
economy_list = attitude_word_dict["economy"]
regulation_list = attitude_word_dict["regulation"]
intervention_list = attitude_word_dict["intervention"]

reform_list = reform_list + market_list



### Calculate Attitude Score ###

economy_score_list = calculate_attitude_score(monthly_series,economy_list)
reform_score_list = calculate_attitude_score(monthly_series,reform_list)
regulation_score_list = calculate_attitude_score(monthly_series,regulation_list)
intervention_score_list = calculate_attitude_score(monthly_series,intervention_list)



score_df = pd.concat([economy_score_list,reform_score_list,regulation_score_list,intervention_score_list],axis=1)
score_df.columns = ["economy","reform","regulation","intervention"]


score_df.to_csv(output_directory+"government_attitude_score_df.csv")




















