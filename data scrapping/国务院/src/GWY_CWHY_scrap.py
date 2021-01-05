
import pandas as pd
import numpy as np
import requests as re
from bs4 import BeautifulSoup
from src.ParserGWY import ParserGWY_CWHY
from src.GWY_news_utils import html_generator
import time
import re as rex



HEADER = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"}
time_sleep = 1
total_page_num = 16
directory = "data/output/"




###############################################################
############### Menu Parser to get the link ###################
###############################################################

menu_df_list = []

for page in range(0,total_page_num):
    
    url = html_generator(page)
    
    response = re.get(url, HEADER, timeout=10)
    response.encoding = "utf-8"
    text = response.text    ### These three steps pull the html content and parse it
    
    parser = ParserGWY_CWHY(text)
    menu_df = parser.single_menu_page_parser() ### Extract the link, title and date from html

    menu_df = parser.second_level_link_update(menu_df,HEADER) ### The link for CWHY need special correction.


    menu_df_list.append(menu_df) ### store the content into dataframe
    
    time.sleep(time_sleep)


menu_df = pd.concat(menu_df_list,axis=0)
menu_df.columns = ["date","title","link"]
menu_df.to_csv(directory+"CWHY_menu_df.csv")



###############################################################
###############################################################
###############################################################


link_list = menu_df.link



total_string_list = []
wrong_list = []

for link in link_list:

    URL = link

    try:
        response = re.get(URL, HEADER, timeout=10)
        response.encoding = "utf-8"
        text = response.text
        html_file = BeautifulSoup(text,"html.parser")

        parser = ParserGWY_CWHY(text)
        total_string = parser.single_content_parser(html_file)

    except:
        
        wrong_list.append(URL)
        total_string = ""
    

    total_string_list.append(total_string)


    time.sleep(1)


menu_df["content"] = total_string_list


menu_df.to_csv(directory+"GWY_CWHY_content.xls")


###### This data need manual revision. There are some website that can not be scrapped. ######



