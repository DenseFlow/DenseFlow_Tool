import numpy as np
import pandas as pd
import os

def myReadData(path):
    f = open(path, 'r')
    a = f.read()
    data = eval(a)
    f.close()
    return data

# 获得从编号->地址的映射关系。输入：原始数据的csv名称
def num_to_addr(casename):
    path = './inputData/AML/data/' + casename + '/all-normal-tx_from.txt'
    dict_from = myReadData(path)
    path = './inputData/AML/data/' + casename + '/all-normal-tx_to.txt'
    dict_to = myReadData(path)
    return dict_from,dict_to

# 获得从地址->编号的映射关系。输入：原始数据的csv名称
def addr_to_num(casename):
    dict_from, dict_to = num_to_addr(casename)
    dict_from = np.array(dict_from)
    dict_to = np.array(dict_to)

    new_dict_from = dict(zip(dict_from[:,1], dict_from[:,0]))
    new_dict_to = dict(zip(dict_to[:,1], dict_to[:,0]))
    return new_dict_from, new_dict_to
# for case in cases:
    
#     tttt = cal_transaction_suscore(source_path+csv_path)
#     tttt.to_csv(source_path+csv_path[0:-4]+'_holo.csv',header=0,index=False)

#trans = pd.read_csv(source_path+csv_path)
def cal_time_sus(X):
    #用户i的可疑度,X为输入的交易数组
    d = len(X)
    J = range(1,d)
    S = 2*np.dot(J,X)/(d*sum(X))-(d+1)/d
    #S是gini系数
    return S
def cal_account_sus(S):
    T = np.mean(S)
    F = 1/(1+np.power(b,T))
    return F
def cal_tran_sus(tran,d=86400):
    #函数输入账户i的交易记录，时间t，切片粒度d默认为前后一天，返回交易可疑度
#     print(tran['value'])
    tol = sum(tran['value'])
    sus = []
    for idx,row in tran.iterrows():
        t = row['timeStamp']
        trand = tran.loc[(tran['timeStamp']>t-d )&(tran['timeStamp']<t+d)]
#         print(trand['value'])
        tol_d = sum(trand['value'])
        if tol != 0:
            sus.append(tol_d/tol)
        else:
            sus.append(0)
    transus = tran
    transus['suspicious_score'] = sus
    return transus

def cal_transaction_suscore(casename,timeinterval=2592000):
    csv_path = './inputData/AML/'+casename+'/all-normal-tx.csv'
    trans = pd.read_csv(csv_path)
    trans[['value']]=trans[['value']].astype(float)
    #1.默认1个月为单位分割周期
    #一周：604800秒
    T = []#记录时间分割节点
    begintime = min(trans['timeStamp'])
    endtime = max(trans['timeStamp'])
    K = int((endtime-begintime)/timeinterval)+1 #计算有几个周期
    print(K,begintime,endtime)
    for i in range(K):
        T.append(begintime + i*timeinterval)
    #接下来遍历T：第k个时间周期
   
    columns_name = trans.columns.values.tolist()
    columns_name.append('suspicious_score')
    Tran_sus = pd.DataFrame(columns = columns_name)
    for k in range(K-1):

        #提取trans中满足
        trank = trans.loc[(trans['timeStamp']>T[k] )&(trans['timeStamp']<T[k+1])]
        trank = cal_tran_sus(trank)
        #print(trank)
        Tran_sus = Tran_sus.append(trank)
        #print(Tran_sus)
    return Tran_sus

#coding=utf-8
# Runs the greedy algorithm.
# Command line arguments: first argument is path to data file. Second argument is path to save output. Third argument (*optional*) is path where the node suspiciousness values are stored.
import numpy as np
import pandas as pd
import os
from random import sample
import datetime

def caldataset(casename):
    #计算当前交易网络的from账户数、to账户数、总账户数
    csv_path = './inputData/AML/'+casename+'/all-normal-tx_sus.csv'
    raw_data = pd.read_csv(csv_path)
    #dict存储 地址：数字的字典映射关系
    #accounts=[]
    dict_from = {}
    dict_to = {}
    count_from = 0
    count_to = 0
    relation = []
    
    n2afrom,n2ato = num_to_addr(casename)
    a2nfrom,a2nto = addr_to_num(casename)
    for line in raw_data.itertuples():
        #只记录交易金额大于等于1的交易
        if float(line[4]) < 1.0:
             continue
        
        getFrom = line[2]
        getTo = line[3]
#         accounts.append(getFrom)
#         accounts.append(getTo)
        getScore = line[12]
        #处理时间数据：
        timeStamp = int(line[5])
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        stdTime = dateArray.strftime("%Y-%m-%d")
#         print(stdTime)
        getTime = stdTime 
        # 构建from和序号的映射
        if not getFrom in dict_from:
            dict_from[getFrom] = count_from
            count_from = count_from + 1
        
        # 构建to和序号的映射
        if not getTo in dict_to:
            dict_to[getTo] = count_to
            count_to = count_to + 1
        # 找到对应的数字
        relation.append([a2nfrom[getFrom],a2nto[getTo],getTime,int(getScore*100),1])
        
        #relation:[from序号，to序号，交易money]的交易记录
        #Holoscope的评分——欺诈评分？
    #考虑frequency？no
#      # 排序
#     relation.sort()
#     # 去重,relation_new为去重后的关系列表
#     relation_new = []
#     relation_new.append(relation[0])
#     new_count = 1
#     #去重
#     for i in relation:
#         if i != relation_new[new_count - 1]:
#             relation_new.append(i)
#             new_count = new_count + 1

#     #不要去重，统计边数
#     relation_count = []
#     relation_count = pd.value_counts(relation)
#     #dict_from = sorted(dict_from.items(),key = lambda x:x[1])
#     #dict_to = sorted(dict_to.items(),key = lambda x:x[1])
    #new
    
    #new
    relationship = pd.DataFrame(relation)
#     relationship.to_csv("easyfihackerholo.csv",header=0,index=False)
    return relationship

def output_holo(casename):
    print(casename,'\n')
    source_path = './inputData/AML/'+casename+'/'
    csv_path = 'all-normal-tx.csv'
    tttt = cal_transaction_suscore(casename)
    suscorefile=source_path+csv_path[0:-4]+'_sus.csv'
    tttt.to_csv(suscorefile,header=0,index=False)
    dddd = caldataset(casename)
    dddd.to_csv(source_path+casename+'_holo.csv')
    print(casename,'完成\n\n\n')