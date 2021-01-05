
import re
from SenAna_Lexicon import SentimentAnalysisLexicon





class SentimentAnalysisText():

	'''
	This class is used to analyze a whole text



	'''




	def __init__(self,text,analyzer,sentence_list=None):

		self.text = text

		if sentence_list is None:
			sentence_list = re.split("。|！|？",text)

		self.sentence_list = sentence_list

		self.num_of_sentence = len(self.sentence_list)

		self.unit_analyzer = analyzer

		self.segmenter = None




	def _count_occurance(self,text):

		word_list = self.segmenter.cut(text)
		self.unit_analyzer.word_list = word_list
		count_dict = self.unit_analyzer.count_number_of_ocurance()
		count = self.unit_analyzer.sentiment_measure(count_dict,count=True)

		return count




	def text_based_sentiment(self):

		count = self._count_occurance(self.text)

		return count


	def sentence_based_sentiment:

		count_list = []

		for sent in self.sentence_list:

			count = self._count_occurance(sent)
			count_list.append(count)

		return count_list





















