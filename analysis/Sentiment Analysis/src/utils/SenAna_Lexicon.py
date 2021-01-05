import jieba
from collections import Counter


class SentimentAnalysisLexicon():

    '''
    This class is used to perform lexicon based sentiment analysis.


    '''

    def __init__(self,text=None,word_list=None,dict_directory=None):
        '''
        This class can be intilized without text or word list. 



        :param text: String
        :param word_list: List(String)

        '''

        self.text = text
        self.word_list = word_list
        self.dict_directory = dict_directory
        self.dict_list = self.load_dict()


    def load_dict(self,encoding = 'gb18030'):
        '''
        This function loads in the dictionary with certain encoding.

        :param dict_dictory: String
        :param encoding: String

        '''

        with open(self.dict_directory,encoding=encoding) as f:
            dict_list = f.readlines()

        dict_list = [word.strip() for word in dict_list]

        return dict_list

    def count_number_of_occurance(self):
        '''
        This function counts the number of times that word in word list occur in the dictionary list.

        :param dict_list: List(String)    

        '''

        if self.word_list is None:
            print("Analyzer Requires a Word List.")

            return None

        c_word = Counter(self.word_list)
        c_dict = Counter(self.dict_list)

        return {word: c_word[word] for word in c_word.keys() & c_dict.keys() }


    def sentiment_measure(self,count_dict,count=True):
        '''
        This function summarizes the number of counts from a count dictionary from function count_number_of_occurance.
        In particular, it summarize the dictionary in two ways. If count=True, it adds up all the occurance. If count=False,
        it only cares how many uniques occurance in the dictionary.

        :param count_dict: Dict{String:int}
        :param count: boolean

        '''

    
        if count:
            num_count = sum(count_dict.values())
        else:
            num_count = len(count_dict.keys())

        return num_count








    












