import pandas as pd
import urllib.request as re
from bs4 import BeautifulSoup
import time
from utils import get_content_finance_department




title_url_directory = "FIN_zcgg_title_url.txt"
header = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}



title_url = pd.read_csv(title_url_directory,encoding="utf-8-sig")

unique_id_list = title_url.iloc[:,0]
url_list = title_url.url


document_list = []
url_error = []

for url in url_list:

    # if the url can be extracted #

    try: 
        document = get_content_finance_department(url,header)

    except:
        document = ""

    if document == "":

    	url_error.append(url)
    	print("Error! : "+url)
    
    document_list.append(document)

    time.sleep(0.2)
        
document_list = pd.Series(document_list)

document_df = pd.concat([unique_id_list,document_list],axis=1)
error_list = pd.Series(url_error)

document_df.to_csv("FIN_zcgg_content.txt")
error_list.to_csv("error.txt")

print("Success!")













