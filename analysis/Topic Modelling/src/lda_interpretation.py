
import pandas as pd
import numpy as np

class LDA_WordAnalyzer():
    
    def __init__(self,model,dictionary):
        
        self.model = model
        self.dictionary = dictionary
    
    
    def get_high_topic_frequency_word(self,topic_number,topn=10):
        

        top_word_list = self.model.get_topic_terms(topic_number,topn=topn)
        
        id_list = [word_tuple[0] for word_tuple in top_word_list]
        word_list = [self.dictionary[idx] for idx in id_list]
        
        return (id_list,word_list)
    
    def get_representative_topic(self,word_id_list):
        
        representative_topic_list = [self.model.get_term_topics(word_id)[0] for word_id in word_id_list]
        
        return representative_topic_list
    
    def word_deviation_ratio(self):
        
        term_topic_distribution = self.model.get_topics()
        term_topic_distribution = pd.DataFrame(term_topic_distribution)
        
        topic_list = range(0,term_topic_distribution.shape[0])
        
        median_list = []
        
        for target in topic_list:
            sub_df = term_topic_distribution[term_topic_distribution.index != target]
            median_list.append(sub_df.median())
        
        median_df = pd.concat(median_list,axis=1).T
        deviation = term_topic_distribution-median_df
        
        ratio_df = deviation/deviation.abs().median()
        
        return ratio_df
        
        
    def double_rank_representative_word(self):
        
        term_topic_distribution = self.model.get_topics()
        term_topic_distribution = pd.DataFrame(term_topic_distribution)
        word_deviation_ratio = self.word_deviation_ratio()

        def rank(x):

        	return x.rank()
        
        rank_term_topic_distribution_df = term_topic_distribution.apply(rank,axis=1)
        rank_word_deviation_ratio_df = word_deviation_ratio.apply(rank,axis=1)
        
        rank_df = rank_term_topic_distribution_df+rank_word_deviation_ratio_df
        
        return rank_df
        
