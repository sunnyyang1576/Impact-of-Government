


import pandas as pd
import numpy as np
import re

from SenAna_Lexicon import SentimentAnalysisLexicon
from jieba_nlp_tools import JiebaNlpTools



policy_directory = "data/policy_text/policy_2.txt"
neg_dict_direct = "data/dictionary/hownet_neg_1.txt"
pos_dict_direct = "data/dictionary/hownet_pos_1.txt"


jieba_tool = JiebaNlpTools()






def sentence_based_sentiment(text):
    
    sentence_list = re.split("。|！",text)
    sentence_list = [sent for sent in sentence_list if sent != ""]
    
    pos_count_list = []
    neg_count_list = []
    
    
    for sent in sentence_list:
        word_list = jieba_tool.cut_sentence(sent,cut_all=True)
        
        pos_senti_analysis = SentimentAnalysisLexicon(text,word_list,pos_dict_direct)
        neg_senti_analysis = SentimentAnalysisLexicon(text,word_list,neg_dict_direct)
    
        pos_count_dict = pos_senti_analysis.count_number_of_occurance()
        pos_count = pos_senti_analysis.sentiment_measure(pos_count_dict,count=True)
    
        neg_count_dict = neg_senti_analysis.count_number_of_occurance()
        neg_count = neg_senti_analysis.sentiment_measure(neg_count_dict,count=True)
    
        pos_count_list.append(pos_count)
        neg_count_list.append(neg_count) 
    
    pos_count_list = pd.Series(pos_count_list)
    neg_count_list = pd.Series(neg_count_list)  
    
    return (pos_count_list,neg_count_list)



#### Load in the dataset ####

with open(policy_directory) as f:
    text = f.read()

text = re.sub("\n","",text)
text = re.sub("\u3000","",text)




#### Text Level Sentiment Count ####

word_list = jieba_tool.cut_sentence(text,cut_all=True)




pos_senti_analysis = SentimentAnalysisLexicon(text,word_list,pos_dict_direct)
pos_count_dict = pos_senti_analysis.count_number_of_occurance()
pos_count = pos_senti_analysis.sentiment_measure(pos_count_dict,count=True)
pos_unique = pos_senti_analysis.sentiment_measure(pos_count_dict,count=False)




neg_senti_analysis = SentimentAnalysisLexicon(text,word_list,neg_dict_direct)
neg_count_dict = neg_senti_analysis.count_number_of_occurance()
neg_count = neg_senti_analysis.sentiment_measure(neg_count_dict,count=True)
neg_unique = neg_senti_analysis.sentiment_measure(neg_count_dict,count=False)


net_ratio = (pos_count-neg_count)/(neg_count+pos_count)
pos_ratio = pos_count/(neg_count+pos_count)
neg_ratio = neg_count/(neg_count+pos_count)







#### Sentence Level Sentiment Count ####

pos_series,neg_series = sentence_based_sentiment(text)
net_series = pos_series - neg_series


sum(net_series>0)/sum(net_series!=0)
sum(net_series>0)/len(net_series)






