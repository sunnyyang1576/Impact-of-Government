
import pandas as pd
import jieba
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim import corpora, models, similarities
from gensim.corpora import Dictionary
import re
import math

from src.nlp_preprocess import NLP_Preprocess, BOW_Filter




def aggregate_preprocess(text,stopwords_list):
    
    word_cut = jieba.cut(text,HMM=True,use_paddle=True,cut_all=False)
    
    word_list = list(word_cut)
    
    pre_processor = NLP_Preprocess(word_list)
    
    pre_processor.remove_punc()
    pre_processor.remove_number()
    pre_processor.remove_single_character()
    pre_processor.remove_stopwords(stopword_list=stopwords_list)
    
    return pre_processor.updated_word_list


def preprocess():

    data_directory = "data/"
    file = "content.csv"
    df = pd.read_csv(data_directory+file)
    df["date"] = pd.to_datetime(df["date"])

    text = list(df["content"])

    stopwords_directory = "data/stopwords/"
    file_1 = "aggregate_stopwords.txt"

    with open(stopwords_directory+file_1,"r",encoding="utf-8") as f:
    
        stopwords_list = f.readlines()
        stopwords_list = [word.strip() for word in stopwords_list]
    
    
    text_after_preprocess = []

    for one_text in text:
    
        if one_text != one_text:
        
            word_list = []
            text_after_preprocess.append(word_list)
        
            continue
    
        word_list = aggregate_preprocess(one_text,stopwords_list)
        text_after_preprocess.append(word_list)

    
    frequency_filter = BOW_Filter(text_after_preprocess)


    wf_low_bound = 2
    df_low_bound = 5


    low_list,high_list = frequency_filter.document_frequency_filter(lower_bound = df_low_bound)
    low_list,high_list = frequency_filter.term_frequency_filter(lower_bound = wf_low_bound)


    frequency_filter.manually_add_filter_words(["中国","总理","李克强"])
    frequency_filter.update_dictionary()

    dictionary = frequency_filter.dictionary

    word_embedding_bow = [dictionary.doc2bow(one_word_list) for one_word_list in text_after_preprocess]


    return word_embedding_bow,dictionary


