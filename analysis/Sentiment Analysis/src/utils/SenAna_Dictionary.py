

import pandas as pd
import numpy as np





def confusion_matrix(test_word,text,label):
    '''
    This function calculates the confusion matrix of the keyword. 
    It returns N11,N10,N01,N00.

    N11: word in text and text is in label
    N10: word in text but text is not in label
    N01: word is not in text but text in label
    N00: word is not in text and text is not in label


    :param test_word: String
    :param text: pd.Series(String)
    :param label: pd.Series(int)

    '''
    
    def func(x):
        
        return test_word in x
    
    in_text = text.apply(func).astype("int32")
    in_label = label.astype("int32")
    
    N11, N10, N01, N00= (0,0,0,0)
    
    for result in zip(in_text,in_label):
        
        if result[0] == result[1]:
            
            if result[0] == 0:
                N00 += 1
            else:
                N11 += 1
        else:
            if result[0] == 0:
                N01 += 1
            else:
                N10 += 1
                
    return (N11,N10,N01,N00)


def chi_square_test(test_word,text,label):
    '''
    This function computes the chi-square test statistics.

    :param test_word: String
    :param text: pd.Series(String)
    :param label: pd.Series(int)

    '''
    
    N11,N10,N01,N00 = confusion_matrix(test_word,text,label)
    
    N = N11+N10+N01+N00

    if ((N11+N01)*(N11+N10)*(N10+N00)*(N01+N00)) == 0:
        
        chi_test_sta = 0

    else:
        chi_test_sta = (N*(N11*N00-N10*N01)**2)/((N11+N01)*(N11+N10)*(N10+N00)*(N01+N00))
    
    return chi_test_sta





def accuracy_precision(test_word,text,label):
    '''
    This function computes the accuracy and precision of the word.

    :param test_word: String
    :param text: pd.Series(String)
    :param label: pd.Series(int)

    '''
    
    N11,N10,N01,N00 = confusion_matrix(test_word,text,label)
    
    if (N11+N10) == 0:

        accuracy = 0
    else:
        accuracy = N11/(N11+N10)
    
    precision = N11/(N11+N01)
    
    return (accuracy,precision)






