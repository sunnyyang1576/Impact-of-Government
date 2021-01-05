import statsmodels.api as sm
import numpy as np
import pandas as pd





score_df_directory = "data/output/score_df.csv"
stock_ret_directory = "data/index_ret.csv"



### Import required dataframe ###




score_df = pd.read_csv("data/output/score_df.csv")
index_df = pd.read_csv("data/index_ret.csv")


index_df.index = pd.to_datetime(index_df.Trddt)
index_df = index_df.iloc[:,1:]
score_df = score_df.iloc[:,1:]


score_df.index = pd.to_datetime(score_df.date)


### Calculate Return ### 

BM_index = index_df.asfreq("BM",method="ffill")
BM_index = BM_index.pct_change()


### Merge score and return dataframe ###

merge_df = BM_index.merge(score_df,how="inner",right_index=True,left_index=True)






### Regression Analysis ###

y = merge_df["I000002"]
x = merge_df.iloc[:,4:]


X,Y = regression_x_y(y,x,y_predict_lag=0,y_include_lag=0,x_include_lag=0)


model = sm.OLS(Y,X)
results = model.fit()
results.summary()


















