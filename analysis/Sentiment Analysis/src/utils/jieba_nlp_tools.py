
import pandas as pd
import numpy as np
import jieba
from collections import Counter
import re

from jieba.analyse import extract_tags
from jieba.analyse import set_stop_words



class JiebaNlpTools():


    def __init__(self,user_dic=None):

        jieba.enable_paddle()
        self.user_dic = user_dic
        if self.user_dic is not None:
            jieba.load_userdict(self.user_dic)
            print("User Dictionary is loaded.")


    def cut_sentence(self,text,cut_all=False,use_paddle=False,min_length=2):

        '''
        This function cuts the sentence into words. 
        It also filters the result based on the length of the word.
        
        
        :param text: string
        :param cut_all: boolean
        :param use_paddle: boolean
        :param min_length: int
        '''

        if self.user_dic is not None:
            jieba.load_userdict(self.user_dic)

        word_cut = jieba.cut(text,cut_all=cut_all,use_paddle=use_paddle)
        word_list = []

        for word in word_cut:
            if len(word)>=min_length:
                word_list.append(word)

        return word_list



    def remove_syntax(self,text,syntax_list,repl=""):
        '''
        This function replace all part of text that follows the list of
        patterns

        :param text: String
        :param syntax_list: List(String)
        :param repl: String

        '''

        for syntax in syntax_list:
            text = re.sub(syntax,"",text)

        return text


    def get_top_n_words(self,word_list,n=2):
        '''
        This function calculates the words with top N highest frequency.

        :param word_list: list(string)
        :param n: int    
        '''

        counter = Counter(word_list)
        top_n = counter.most_common(n)

        return top_n


    def filter_stopwords(self,word_list,stopword_list):
        '''
        This function filter out the stopwords.

        :param word_list: list(string)
        :param stopword_list: list(string)

        '''

        word_list = [word for word in word_list if word not in stopword_list]

        return word_list



    def tf_idf(self,text,n,stopwords_dir,allowPOS=None):
        '''
        This function calculates the tf-idf keywords.

        '''

        set_stop_words(stopwords_dir)
        tags = extract_tags(sentence=text, topK=n, withWeight=True,allowPOS=allowPOS)

        return tags


























