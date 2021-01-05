

import urllib.request as re
from bs4 import BeautifulSoup
import pandas as pd



def get_titles_url_finance_department(url,header,url_stem):



    # this part send the request, pull and decompose the html form the response #
    req = re.Request(url=url,headers=header)
    res = re.urlopen(req)
    html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    

    # this part extract the body part of the html #
    body = soup.body

    # this part extract the main title box in the body part #
    titles = body.find_all("div",{"class": "mainboxerji"})[0]
    title_box_list = titles.find_all("ul",{"class": "xwfb_listbox"})
    
    
    # from each title box, it extract the timestamp, the title and url #
    title_list = []
    timestamp_list = []
    
    for title_box in title_box_list:
        title = title_box.find_all("a")
        timestamp = title_box.find_all("span")
        
        title_list+=title
        timestamp_list += timestamp
    
    content_url_list = []
    content_title_list = []
    
    for title in title_list:
        
        content_url = title.get("href")
        content_title = title.get("title")


        if content_url.startswith("./"):
            content_url = url_stem+content_url[2:]
        
        content_url_list.append(content_url)
        content_title_list.append(content_title)
        
    timestamp_list = [timestamp.string for timestamp in timestamp_list]
    
    
    # this part save them into a dataframe #
    content_url_list = pd.Series(content_url_list)
    content_title_list = pd.Series(content_title_list)
    timestamp_list = pd.Series(timestamp_list)
    
    all_titles = pd.concat([timestamp_list,content_title_list,content_url_list],axis=1)
    all_titles.columns = ["timestamp","title","url"]
    
    return all_titles
    
 

def create_unique_id(department,sector,start,end):
    '''

    This function creates a unique list of id for each government text.

    :param department: string (higher case)
    :param sector: string (lower case)
    :param start: int
    :param end: int
    '''
    
    id_list = [department + "_"+ sector + "_" + str(idx) for idx in range(start,end)]
    id_list = pd.Series(id_list)
    
    return id_list




def get_content_finance_department(url,header):


    req = re.Request(url=url,headers=header)
    res = re.urlopen(req)
    html = res.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    body = soup.body



    main_box = body.find("div",{"class":"mainboxerji"})
    if main_box is not None:
        main_box = main_box.find("div",{"class":"box_content"})
    if main_box is not None:
        main_box = main_box.find("div",{"class":"my_conboxzw"})
    if main_box is not None:
        main_box = main_box.find("div",{"class":"TRS_Editor"})
    if main_box is not None:
        content_list = main_box.find_all("p")
    elif main_box is None:
        content_list = []


    document = ""
    for content in content_list:
        content = content.string
        if content is None:
            content = ""
        document+=content
    return document
















    

