


if __name__ == "__main__":



    # import required library #
	import pandas as pd
	from utils import get_titles_url_finance_department,create_unique_id
	import time




    # obtain the required parameters #
	url_stem = r'http://www.mof.gov.cn/zhengwuxinxi/zhengcefabu/'
	header = {"User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
	start_page_num = 1
	end_page_num = 20

	depart = "FIN"
	sector = "zcgg"
	start_idx = 0
	sleep_time = 1

    
    
    # create url list based on parameters given #
    
	url_list = [url_stem+"index_"+str(idx)+".htm" for idx in range(start_page_num,end_page_num)]
	url_list.insert(0,url_stem+"index.htm")


    # pull the content and store them as df # 
	df_list = []
	for url in url_list:
		print(url)
		result_df = get_titles_url_finance_department(url,header,url_stem)
		df_list.append(result_df)
		time.sleep(sleep_time)
	result = pd.concat(df_list,axis=0)
	result.index = create_unique_id(department=depart,sector=sector,start=start_idx,end=start_idx+result.shape[0])


    # output the result #
	result.to_csv("FIN_zcgg_title_url.txt",index=True,encoding="utf-8-sig")


	# print # 
	print("Running Successfully.")






















