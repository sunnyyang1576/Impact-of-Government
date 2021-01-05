
import pandas as pd
import re
from gensim.corpora import Dictionary



class NLP_Preprocess():


    def __init__(self,word_list):

        self.ori_word_list = word_list
        self.updated_word_list = word_list


    def remove_punc(self):

        punc = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
        word_list = [word for word in self.updated_word_list if word not in punc]

        self.updated_word_list = word_list

    def remove_number(self):

        word_list = [re.sub(r'[0-9]+', '', word) for word in self.updated_word_list]

        self.updated_word_list = word_list


    def remove_single_character(self):

        word_list = [word for word in self.updated_word_list if len(word)>1]

        self.updated_word_list = word_list


    def remove_stopwords(self,stopword_list):

        word_list = [word for word in self.updated_word_list if word not in stopword_list]

        self.updated_word_list = word_list






class BOW_Filter():


	def __init__(self,corpus):

		self.ori_corpus = corpus
		self.update_corpus = corpus

		self.dictionary = Dictionary(corpus)

		self.filter_word_list = []


	def term_frequency_filter(self,lower_bound=None,upper_bound=None):

		term_frequency = pd.Series(self.dictionary.cfs)

		low_list = []
		high_list = []

		if lower_bound is not None:

			low_list = list(term_frequency[term_frequency<lower_bound].index)

		if upper_bound is not None:

			high_list = list(term_frequency[term_frequency>upper_bound].index)

		self.filter_word_list += low_list
		self.filter_word_list += high_list
		self.filter_word_list = list(set(self.filter_word_list))

		return (low_list,high_list)

	def document_frequency_filter(self,lower_bound=None,upper_bound=None):

		document_frequency = pd.Series(self.dictionary.dfs)

		low_list = []
		high_list = []

		if lower_bound is not None:

			low_list = list(document_frequency[document_frequency<lower_bound].index)

		if upper_bound is not None:

			high_list = list(document_frequency[document_frequency>upper_bound].index)

		self.filter_word_list += low_list
		self.filter_word_list += high_list
		self.filter_word_list = list(set(self.filter_word_list))

		return (low_list,high_list)



	def show_filter_word(self):

		word_list = []

		for idx in self.filter_word_list:

			word_list.append(self.dictionary[idx])

		return word_list


	def update_dictionary(self):

		self.dictionary.filter_tokens(bad_ids=self.filter_word_list)



	def manually_add_filter_words(self,word_list):

		new_list = []

		for word in word_list:

			if word not in self.dictionary.token2id.keys():

				continue

			new_idx = self.dictionary.token2id[word]

			new_list.append(new_idx)

		self.filter_word_list += new_list
		self.filter_word_list = list(set(self.filter_word_list))



































