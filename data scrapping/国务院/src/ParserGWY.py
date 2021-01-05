


import pandas as pd
from bs4 import BeautifulSoup
import re as regex
import requests as re



class Parser():
    
    
    def __init__(self,text):
        
        self.text = text

    def single_menu_page_parser(self):
        
        pass
    
    
    def single_element_parser(self,element):
        
        pass






class ParserGWY(Parser):

    def __init__(self,text):
        
        html_file = BeautifulSoup(text,"html.parser")
        
        super().__init__(html_file)


    def single_menu_page_parser(self):

    	pass


    def single_element_parser(self,element):

    	pass





class ParserGWY_GWYXW(ParserGWY):

	def __init__(self,text):

		super().__init__(text)



	def single_menu_page_parser(self):

		date_list = []
		title_list = []
		link_list = []

		news_box = self.text.find("div",{"class":"list list_1 list_2"})
		news_list = news_box.find_all("li")

		for news in news_list:

			date,title,link = self.single_element_parser(news)

			date_list.append(date)
			title_list.append(title)
			link_list.append(link)

		date_list = pd.Series(date_list)
		title_list = pd.Series(title_list)
		link_list = pd.Series(link_list)

		df = pd.concat([date_list,title_list,link_list],axis=1)

		return df


	def single_element_parser(self,element):

		title = element.a.string
		link = element.a.get("href")
		date = element.span.string
		date_list = date.split(".")
		date = "-".join(date_list)

		return (date,title,link)





class ParserGWY_CWHY(ParserGWY):

	def __init__(self,text):

		super().__init__(text)


	def single_menu_page_parser(self):

		date_list = []
		title_list = []
		link_list = []

		news_box = self.text.find("div",{"class":"list list_1 list_2"})
		news_list = news_box.find_all("li")


		for news in news_list:

			date,title,link = self.single_element_parser(news)
			date_list.append(date)
			title_list.append(title)
			link_list.append(link)

		date_list = pd.Series(date_list)
		title_list = pd.Series(title_list)
		link_list = pd.Series(link_list)

		df = pd.concat([date_list,title_list,link_list],axis=1)

		return df


	def single_element_parser(self,element):

		link = element.a.get("href")
		date = element.span.string


		if element.a.string is not None:

			title = element.a.string

		else:

			title_list = list(element.a.strings)

			title = " ".join(title_list)


		date_list = date.split(".")
		date = "-".join(date_list)

		return (date,title,link)



	def second_level_link_update(self,menu_df,HEADER):

		new_link_list = []

		link_list = menu_df.iloc[:,2]

		for link in link_list:

			response = re.get(link, HEADER, timeout=10)
			response.encoding = "utf-8"
			text = response.text
			html_file = BeautifulSoup(text,"html.parser")

			url_list = html_file.find_all("a",{"target":"_blank"})
			url = [url.get("href") for url in url_list if url.string == '[详细内容]']

			if len(url) != 0:
				link = url[0]

			if link.startswith(".."):
				link = regex.sub("\.{2}","http://www.gov.cn/guowuyuan",link)

			new_link_list.append(link)

		menu_df.iloc[:,2] = new_link_list

		return menu_df


	def single_content_parser(self,html_file):

		string_list = []

		try:

			content = html_file.find("div",{"class":"content"})
			p_list = content.find_all("p")
			string_list = [p.string for p in p_list if p.string is not None]

		except:

			try:
				content = html_file.find("div",{"class":"pages_content"})
				p_list = content.find_all("p")
				string_list = [p.string for p in p_list if p.string is not None]

			except:

				print("Wrong !")


		total_string = " ".join(string_list)

		return total_string













































        









