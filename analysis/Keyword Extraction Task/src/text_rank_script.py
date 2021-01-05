import pandas as pd
import numpy as np

import networkx as nx

from os import listdir
import re

import plotly.offline as py
import plotly.graph_objects as go


from text_rank import TextRank


text_directory = "data/policy_text/"



# This part loads in the text and select one as sample text

policy_dir = listdir(text_directory)

text_list = []

for file in policy_dir:
    file = text_directory+file
    
    with open(file,"r+")  as f:
        text = f.read()
    
    text = re.sub("\n","",text)
    text = re.sub("\u3000","",text)
    
    text_list.append(text)


sample_text = text_list[1]



# set up the text rank parameters

allowPOS = ["n"]
stopwords = ["为了"]
span = 3





# This part implements the Text rank algorithm

## initilization
tr_keyword = TextRank(allowPOS,stopwords,span)

## implement the text rank
tr_keyword.text_rank(sample_text,10)



# Text relationship Study

## cut the text into list of words
word_pair = tr_keyword._cut(sample_text)


## create the co-occurance matrix (this is for )
co_graph = tr_keyword.co_occurance_matrix(word_pair)
df = tr_keyword.co_occur_graph_to_matrix(co_graph,normalization=True)


## Visulize the text graph

word_list = list(df.columns)


name_dict = {}
for i in range(len(word_list)):
    
    name_dict[i] = word_list[i]


nx_graph = nx.from_numpy_array(df.values)
nx_graph = nx.relabel_nodes(nx_graph,name_dict)  

### Use the NX graphing function
nx.draw_networkx(nx_graph, font_family='SimHei', node_size=1)




### Use the Plotly graphing function

#### Filter the edge with low weight
for edge in nx_graph.edges():
    
    if nx_graph.edges()[edge]['weight'] < 0.17:
        
        nx_graph.edges()[edge]['weight'] = 0


pos_ = nx.spring_layout(nx_graph)



#### Create the edge plot

def make_edge(x, y, text, width):
    return  go.Scatter(x         = x,
                       y         = y,
                       line      = dict(width = width,
                                   color = 'cornflowerblue'),
                       hoverinfo = 'text',
                       text      = ([text]),
                       mode      = 'lines')




edge_trace = []

for edge in nx_graph.edges():

	if nx_graph.edges()[edge]['weight'] > 0:

		char_1 = edge[0]
		char_2 = edge[1]


		x0, y0 = pos_[char_1]
		x1, y1 = pos_[char_2]

		text   = char_1 + '--' + char_2 + ': ' + str(nx_graph.edges()[edge]['weight'])

		trace  = make_edge([x0, x1, None], [y0, y1, None], text, 
                           width = 0.3*nx_graph.edges()[edge]['weight']**1.75)


		edge_trace.append(trace)


#### Create the node plot

node_trace = go.Scatter(x         = [],
                        y         = [],
                        text      = [],
                        textposition = "top center",
                        textfont_size = 10,
                        mode      = 'markers+text',
                        hoverinfo = 'none',
                        marker    = dict(color = [],
                                         size  = [],
                                         line  = None))



for node in nx_graph.nodes():
    x, y = pos_[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])
    node_trace['marker']['color'] += tuple(['cornflowerblue'])
    node_trace['marker']['size'] += tuple([5*1]) # this could control the size of node (could have size varying with weight)
    node_trace['text'] += tuple(['<b>' + node + '</b>'])




#### Set the layout

layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)', # transparent background
    plot_bgcolor='rgba(0,0,0,0)', # transparent 2nd background
    xaxis =  {'showgrid': False, 'zeroline': False}, # no gridlines
    yaxis = {'showgrid': False, 'zeroline': False}, # no gridlines
)



fig = go.Figure(layout = layout)
#### Add all edge traces
for trace in edge_trace:
    fig.add_trace(trace)

#### Add node trace
fig.add_trace(node_trace)

#### Remove legend
fig.update_layout(showlegend = False)

#### Remove tick labels
fig.update_xaxes(showticklabels = False)
fig.update_yaxes(showticklabels = False)

#### Show figure
fig.show()




# K-Cores Decomposition

k_core_graph = nx.k_core(nx_graph,k=4)

k_core_graph.nodes()


























