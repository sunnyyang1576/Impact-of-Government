import os




dictionary_directory = "dictionary/ref_dictionary/"


dictionary_list = os.listdir(dictionary_directory)[1:] # get all the file name of the attitude lexicon


dict_list = []

for dictionary in dictionary_list: # read the lexicon and store them in a list 
     
    f = open(dictionary_directory+dictionary) 
    dict_add = f.readlines()
    dict_list += dict_add
    f.close()

dict_list = [word.strip() for word in dict_list]
dict_list = [word for word in dict_list if len(word)>0]




with open("user_defined_dict.txt","w") as f:
    
    for word in dict_list:
        
        f.write(word)
        f.write("\n")


