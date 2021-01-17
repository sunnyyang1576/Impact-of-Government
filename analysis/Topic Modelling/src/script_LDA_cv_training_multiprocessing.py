

import pandas as pd
import numpy as np
import gensim
import time
import multiprocessing as mp

from utils_preprocess import preprocess




def model_training(train_data,test_data,param):
    
    lda_model = gensim.models.ldamodel.LdaModel(corpus=train_data,**param)
    log_perplexity = lda_model.log_perplexity(test_data)
    
    return log_perplexity


def create_cv_data(word_embedding,n_fold,random_seed):
    
    np.random.seed(random_seed)
    size_of_document = len(word_embedding)
    random_index_group = np.random.randint(0,n_fold,size_of_document)
    
    data_list = []
    
    for fold in range(0,n_fold):
        
        test_data = []
        train_data = []
        
        for idx,document in zip(random_index_group,word_embedding):
            
            if idx == fold:
                
                test_data.append(document)
            
            else:
                
                train_data.append(document)
        
        data_list.append((train_data,test_data))
    
    return data_list


def multiprocessing_lda_training(data_list,param):

    print("Start a cv work.")
    
    perplexity_list = []
    
    for train_data,test_data in data_list:
        
        perplexity = model_training(train_data,test_data,param)
        perplexity_list.append(perplexity)
    
    return np.mean(perplexity_list)


def perplexity_callback(x):

    result_list.append(x)






if __name__ == "__main__":

    #### Preprocess the data ####

    word_embedding_bow,dictionary = preprocess()


    #### Set the parameter for the cv training ####
    
    topic_num_list = range(50,100,2)

    n_fold = 5
    random_seed = 150
    n_process = 40

    word_embedding = word_embedding_bow
    dictionary = dictionary
    
    param = {"num_topics":1,
             "id2word":dictionary,
             "random_state":10,
             "chunksize":1,
             "passes":1,
             "alpha":'auto',
             "eta":"auto"}

    
    print("Create work.")

    data_list = create_cv_data(word_embedding,n_fold,random_seed) ### this creates the cross-validation dataset
    
    param_list = []  ### this creates the parameter grid for the cross-validation dataset

    for topic in topic_num_list:
        param["num_topics"] = topic
        param_list.append(param.copy())


    

    result_list = []


    print("Start to assign work")
    

    pool = mp.Pool(n_process)  

    for param in param_list:

        pool.apply_async(multiprocessing_lda_training, args=(data_list,param), callback = perplexity_callback)

    
    print("Work Start.")

    pool.close()
    pool.join()

    print("Work Finished.")


    with open("data/result/topic_number_cv_list.txt","w+") as f:
        for result in result_list:

            f.write(str(result))
            f.write("\n")


































