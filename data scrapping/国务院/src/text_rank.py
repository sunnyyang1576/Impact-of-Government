import pandas as pd
import numpy as np

import jieba
import jieba.analyse

import networkx as nx
from collections import defaultdict
import sys


class UndirectedWeightedGraph():
    
    d = 0.85
    max_iteration = 20
    
    
    def __init__(self):
        
        self.graph = defaultdict(list)
          
    
    
    def addEdge(self,start,end,weight):
        
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))
    
    
    
    def rank(self):
        
        ws = defaultdict(float)
        outSum = defaultdict(float)
        
        wsdef = 1.0 / (len(self.graph) or 1.0)
        
        for key,list_tup in self.graph.items():
            
            ws[key] = wsdef
            outSum[key] = sum((tup[2] for tup in list_tup),0.0)
        
        
        sorted_keys = sorted(self.graph.keys())
        
        for x in range(self.max_iteration):
            
            for key in sorted_keys:
                
                summation = 0
                
                for edge_tuple in self.graph[key]:
                    
                    summation += edge_tuple[2]/outSum[edge_tuple[1]] * ws[edge_tuple[1]]
                
                ws[key] = (1-self.d) + self.d*summation
        
        
        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])
        
        for w in ws.values():
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w
        
        
        for n, w in ws.items():
            
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        return ws
                






class TextRank():

    def __init__(self,allowPOS,stopwords,span):

        self.allowPOS = allowPOS
        self.stopwords = stopwords
        self.span = span

    def _cut(self,text):

        word_pair = tuple(jieba.posseg.dt.cut(text))

        return word_pair


    def _filter_word(self,word,POS,min_len=2):

        return (word not in self.stopwords) and (POS in self.allowPOS) and (len(word) >= min_len)



    def co_occurance_matrix(self,word_pair):

        co_occur_mat = defaultdict(int)

        for i,word_pos in enumerate(word_pair):

            word,pos = word_pos

            if self._filter_word(word,pos):

                for j in range(i+1,i+self.span):

                    if j >= len(word_pair):

                        break

                    surrounding_word, surrounding_pos = word_pair[j]

                    if not self._filter_word(surrounding_word,surrounding_pos):

                        continue

                    co_occur_mat[(word,surrounding_word)] += 1


        graph = UndirectedWeightedGraph()

        for vertexes,weight in co_occur_mat.items():

            graph.addEdge(vertexes[0],vertexes[1],weight)

        return graph



    def co_occur_graph_to_matrix(self,graph,normalization=True):

    	word_list = list(graph.graph.keys())
    	length = len(word_list)

    	matrix = pd.DataFrame(np.zeros([length,length]))
    	matrix.columns = word_list
    	matrix.index = word_list

    	for start in word_list:

    		tuple_list = graph.graph[start]

    		for tup in tuple_list:

    			end = tup[1]
    			weight = tup[2]

    			matrix.loc[start,end] = weight

    	if normalization:

    		matrix = matrix/matrix.values.max()

    	return matrix



    def text_rank(self,text,topN):


        word_pair = self._cut(text)
        co_occur_graph = self.co_occurance_matrix(word_pair)

        ws = co_occur_graph.rank()

        def func(x):
            return x[1]

        tags = sorted(ws.items(), key=func, reverse=True)

        return tags[:topN]



























