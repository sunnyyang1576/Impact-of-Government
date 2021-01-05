import pandas as pd
import numpy as np
from src.utils.SenAna_Dictionary import chi_square_test,accuracy_precision



def group_chi_square_test(seed_list,text,label_reform,label_market,label_intervention,label_regulation):
    
    reform_test = []
    market_test = []
    intervention_test = []
    regulation_test = []

    for test_word in seed_list:
        result_reform = chi_square_test(test_word,text,label_reform)
        result_market = chi_square_test(test_word,text,label_market)
        result_intervention = chi_square_test(test_word,text,label_intervention)
        result_regulation = chi_square_test(test_word,text,label_regulation)
        
        reform_test.append(result_reform)
        market_test.append(result_market)
        intervention_test.append(result_intervention)
        regulation_test.append(result_regulation)
    
    reform_test = pd.Series(reform_test)
    market_test = pd.Series(market_test)
    intervention_test = pd.Series(intervention_test)
    regulation_test = pd.Series(regulation_test)
    
    result_df = pd.concat([reform_test,market_test,intervention_test,regulation_test],axis=1)
    result_df.index = seed_list
    result_df.columns = ["reform","market","intervention","regulation"]
    result_df = result_df.round(2)
    
    return result_df


def group_accuracy_precision(seed_list,text,label):
    
    accuracy_list = []
    precision_list = []
    
    for word in seed_list:
        
        accuracy,precision = accuracy_precision(word,text,label)
        accuracy_list.append(accuracy)
        precision_list.append(precision)
    
    accuracy_list = pd.Series(accuracy_list)
    precision_list = pd.Series(precision_list)
    
    acc_pre_df = pd.concat([accuracy_list,precision_list],axis=1)
    acc_pre_df.index = seed_list
    acc_pre_df.columns = ["Accuracy","Precision"]
    
    return acc_pre_df


test_set_directory = "output/sentiment样本.xlsx"
df = pd.read_excel(test_set_directory)
df = df.fillna(0)
df.iloc[:,0:4] = df.iloc[:,0:4].astype('int32')


reform_seed_list = ["改革","改善","转变","创新","探索","重构","废止","简化","适应","修改","修订"]
market_seed_list = ["公平","市场","公开","竞争","高效","灵活","资源配置","减少政府","积极性","民间投资","自主","招标","中标"]
intervention_seed_list = ["政府购买","政府采购","政府投资","介入","干预","担保","减税","降费","减轻","支持","鼓励","激励",
                          "引导","调节","集中采购","招标采购","扶持","购买服务","统筹","整合"]
regulation_seed_list = ["监督","管理","质疑","投诉","规定","规范","处理","处罚","追究","明确","检查","考核","完善","指导","建立健全",
                        "规则","加强","限制","督促","监控"]




text = df.iloc[:,4]

label_reform = df.iloc[:,0]
label_market = df.iloc[:,1]
label_intervention = df.iloc[:,2]
label_regulation = df.iloc[:,3]




reform_chi = group_chi_square_test(reform_seed_list,text,label_reform,label_market,label_intervention,label_regulation)
market_chi = group_chi_square_test(market_seed_list,text,label_reform,label_market,label_intervention,label_regulation)
intervention_chi = group_chi_square_test(intervention_seed_list,text,label_reform,label_market,label_intervention,label_regulation)
regulation_chi = group_chi_square_test(regulation_seed_list,text,label_reform,label_market,label_intervention,label_regulation)


reform_acc = group_accuracy_precision(reform_seed_list,text,label_reform)
market_acc = group_accuracy_precision(market_seed_list,text,label_market)
intervention_acc = group_accuracy_precision(intervention_seed_list,text,label_intervention)
regulation_acc = group_accuracy_precision(regulation_seed_list,text,label_regulation)



reform_chi.to_excel("output/chi_test_reform.xlsx")
market_chi.to_excel("output/chi_test_market.xlsx")    
intervention_chi.to_excel("output/chi_test_intervention.xlsx")    
regulation_chi.to_excel("output/chi_test_regulation.xlsx")


reform_acc.to_excel("output/acc_reform.xlsx")
market_acc.to_excel("output/acc_market.xlsx")
intervention_acc.to_excel("output/acc_intervention.xlsx")
regulation_acc.to_excel("output/acc_regulation.xlsx")








