import pandas as pd
import numpy as np
import requests as re
from bs4 import BeautifulSoup
from ParserGWY import ParserGWY_GWYXW
import time
from GWY_news_utils import GWY_URL_generator,premier




HEADER = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
time_sleep = 1
total_page_num = 508
directory = "data/output"




### Menu Page Scrapping ###

df_list = []

for page_number in range(1,total_page_num):
    
    if page_number % 100 == 0:

    	print("Processing: {}".format(page_number))
    
    
    URL = GWY_URL_generator(page_number)
    
    try:
        response = re.get(URL, HEADER, timeout=10)
        response.encoding = "utf-8"
        text = response.text
        parser = ParserGWY_GWYXW(text)
        df = parser.single_menu_page_parser()
        df_list.append(df)
    
    except:
        print("Error at page"+ str(page_number))
    
    time.sleep(time_sleep)



title_df = pd.concat(df_list)
title_df.columns = ["date","title","link"]

title_df.to_csv(directory+"GWY_news_title.csv")

print("Menu Page Scrapping Successed.")






### Content Page Scrapping ###

title_df = pd.read_csv("GWY_news_title.csv")
title_df = title_df.iloc[:,1:]


premier_df = title_df[title_df.iloc[:,2].apply(premier)]
premier_df.index = range(0,len(premier_df))


total_string_list = []
wrong_list = []
for link in premier_df.link:
    
    URL = link
    
    try:
        response = re.get(URL, HEADER, timeout=10)
        response.encoding = "utf-8"
        text = response.text
        html_file = BeautifulSoup(text,"html.parser")
        content = html_file.find("div",{"class":"content"})
        p_list = content.find_all("p")
        string_list = [p.string for p in p_list if p.string is not None]
    except:
        wrong_list.append(URL)
        string_list = []
    
    
    total_string = ""
    
    for string in string_list:
        
        total_string += string
    
    total_string_list.append(total_string)




premier_df["content"] = total_string_list
premier_df["date"] = pd.to_datetime(premier_df.date)


premier_df.to_csv(directory+"GWY_premier_news_content.csv")

print("Content Page Scrapping Successed.")




