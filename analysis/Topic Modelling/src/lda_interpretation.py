
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
        
        representative_topic_list = [self.model.get_term_topics(word_id)[0] for word_id in word_id_list if len(self.model.get_term_topics(word_id)) > 0]
        
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
        





class LDA_DocumentAnalyzer():
    
    def __init__(self,model,word_embedding,word_list,actual_document):
        
        self.model = model
        self.word_embedding = word_embedding
        self.document_list = actual_document
        self.word_list = word_list
    
    def create_document_topic_distribution(self):
        
        doc_topic_distribution = [self.model.get_document_topics(doc) for doc in self.word_embedding]
        
        aggregate_topic_list = []
        
        for doc in doc_topic_distribution:
            
            topic_list = []
            
            for topic in doc:
                
                topic_list.append(topic[1])
                
            topic_list = pd.Series(topic_list)
            
            aggregate_topic_list.append(topic_list)
        
        aggregate_topic_df = pd.concat(aggregate_topic_list,axis=1).fillna(0)
        
        return aggregate_topic_df
    
    def create_deviation_ratio_df(self):
        
        aggregate_topic_df = self.create_document_topic_distribution()
        
        topic_list = range(0,aggregate_topic_df.shape[0])
        
        median_list = []
        
        for target in topic_list:
            
            sub_df = aggregate_topic_df[aggregate_topic_df.index != target]
            
            median_list.append(sub_df.median())
        
        median_df = pd.concat(median_list,axis=1).T
        
        deviation = aggregate_topic_df-median_df
        
        ratio_df = deviation/deviation.abs().median()
        
        return ratio_df
    
    
    def create_double_rank(self):
        
        aggregate_topic_df = self.create_document_topic_distribution()
        deviation_ratio_df = self.create_deviation_ratio_df()
        
        def rank(x):
            
            return x.rank()
        
        
        aggregate_topic_rank = aggregate_topic_df.apply(rank,axis=1)
        deviation_ratio_rank = deviation_ratio_df.apply(rank,axis=1)
        
        
        return aggregate_topic_rank+deviation_ratio_rank
    
    
    
    def get_n_representative_document(self,indicator,topn=10):
        
        index_list = list(indicator.nlargest(topn).index)
        
        document_list = [self.document_list[idx] for idx in index_list]
        
        word_list = [self.word_list[idx] for idx in index_list]
        
        return (word_list,document_list)
    
    
    def get_n_representative_document_high_frequency(self,topic_num,topn=10):
        
        aggregate_topic_df = self.create_document_topic_distribution()
        
        indicator = aggregate_topic_df.iloc[topic_num,:]
        
        word_list,document_list = self.get_n_representative_document(indicator,topn)
        
        return (word_list,document_list)
    
    def get_n_representative_document_high_double_rank(self,topic_num,topn=10):
        
        rank_df = self.create_double_rank()
        
        indicator = rank_df.iloc[topic_num,:]
        
        word_list,document_list = self.get_n_representative_document(indicator,topn)
        
        return (word_list,document_list)
    
        
        
        
        
        





