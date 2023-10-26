#coding=utf-8
# Runs the greedy algorithm.
# Command line arguments: first argument is path to data file. Second argument is path to save output. Third argument (*optional*) is path where the node suspiciousness values are stored.
import numpy as np
import pandas as pd
import os
from random import sample
from Code.info import *
# csvtodata(csv_path)    将原始csv里的from\to地址转化编号，并存储映射关系。输入：csv路径
# myReadData(path)       读取单个映射关系文件。输入：文件路径
# num_to_addr(csvname)   获得从编号->地址的映射关系。输入：原始数据的csv名称
# addr_to_num(csvname)   获得从地址->编号的映射关系。输入：原始数据的csv名称

# saveaddr(csvname,ifrows,data)   保存运算结果的实际地址。输入：原始数据的csv名称、是否为行、子集的编号
# 使用方法：saveaddr(csvname,1,lwRes[0][0])
#         saveaddr(csvname,0,lwRes[0][1])

# checkans(csvname,Hacksname)   结果验证，查看结果中标有洗钱地址的数量。输入：原始数据的csv名称、可疑节点所在csv

# 将原始csv里的from\to地址转化编号，并存储映射关系。输入：csv路径
# 思路：设置两个字典from字典、to字典，存储键值

#三步转账数据集构建：首先划分起点A、中间M、终点账户C集合
def diff(listA,listB):
    #求交集的两种方式
    retA = [i for i in listA if i in listB]
    retB = list(set(listA).intersection(set(listB)))
    
    return retA
def CHA(listA,listB):
    #B-A
    #求差集，在B中但不在A中
    retD = list(set(listB).difference(set(listA)))
    return retD

def BING(listA,listB):
    retC = list(set(listA).union(set(listB)))
    return retC

# 读取单个映射关系文件。输入：文件路径
def myReadData(path):
    f = open(path, 'r')
    a = f.read()
    data = eval(a)
    f.close()
    return data

# 获得从编号->地址的映射关系。输入：原始数据的csv名称
def num_to_addr(casename):
    path = './inputData/AML/data/' + casename + '/all-normal-tx_A.txt'
    dict_A = myReadData(path)
    path = './inputData/AML/data/' + casename + '/all-normal-tx_H.txt'
    dict_H = myReadData(path)
    path = './inputData/AML/data/' + casename + '/all-normal-tx_B.txt'
    dict_B= myReadData(path)
    return dict_A,dict_H,dict_B

# 获得从地址->编号的映射关系。输入：原始数据的csv名称
def addr_to_num(casename):
    dict_A, dict_H,dict_B = num_to_addr(casename)
    dict_A= np.array(dict_A)
    dict_H = np.array(dict_H)
    dict_B = np.array(dict_B)

    new_dict_A = dict(zip(dict_A[:,1], dict_A[:,0]))
    new_dict_H = dict(zip(dict_H[:,1], dict_H[:,0]))
    new_dict_B = dict(zip(dict_B[:,1], dict_B[:,0]))
    return new_dict_A, new_dict_H, new_dict_B

def caldataset(casename,setting1=10,setting2 = 2):
    #计算当前交易网络的from账户数、to账户数、总账户数
    csv_path = './inputData/AML/'+casename+'/all-normal-tx.csv'
    raw_data = pd.read_csv(csv_path)
    raw_data[['value']] = raw_data[['value']].astype(float)
    raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)

    account_from = raw_data['from'].tolist()
    account_to = raw_data['to'].tolist()
    account_total = BING(account_from,account_to)
    
    AccA = []
    AccM = []
    AccC = []
    #划分三部图
    print('划分三部图...\n')
    for curadd in account_total:
    #转出交易：从curadd转出
        tmptran = raw_data[raw_data['from']==curadd]
        Chusum = len(tmptran)
        #转入交易：转入到curadd
        tmptran = raw_data[raw_data['to']==curadd]
        Rusum = len(tmptran)
        #print(curadd,':','转出次数:',Chusum,'转入次数',Rusum)
        #转出比转入大
        if Chusum > Rusum*setting1:
            AccA.append(curadd)
        if Rusum > Chusum*setting1:
            AccC.append(curadd)
        if Chusum> setting2 and Rusum>setting2:
            AccM.append(curadd)
        else :
            AccM.append(curadd)
    print('完毕...')
    #现在构建第一步交易and第二步交易
    #relation[i][j]j=0,1,2
    print(casename)
    print("出发：",len(AccA),"中间",len(AccM),"终点",len(AccC))
    print('当前数据集交易总数:',len(raw_data))
   # for a in account_A:#a是一个地址，要找到所有relation里面a出发的，到达M的交易
    xy_tran=[]
    yz_tran = []
    triA = {}#n2a
    triH = {}
    triB = {}
    a2nA = {}
    a2nH = {}
    a2nB = {}
    Ac =0
    Hc =0
    Bc =0
    print('遍历中...')
    for idx,data in raw_data.iterrows():
        #只记录交易金额大于等于1的交易
        if data['value'] ==0.0:
             continue
        getFrom = data['from']
        getTo = data['to']
#         accounts.append(getFrom)
#         accounts.append(getTo)
        getMoney = data['value']*1e-18
        getTime = data['timeStamp']
        if (getFrom in AccA) and (getTo in AccM):
            
            if not getFrom in list(triA.values()):
                #如果当前from地址未加入则加入
                triA[Ac]=getFrom
                a2nA[getFrom]=Ac
                Ac+=1
            if not getTo in list(triH.values()):
                #如果当前from地址未加入则加入
                triH[Hc]=getTo
                a2nH[getTo] = Hc
                Hc+=1
            relation = [a2nA[getFrom],a2nH[getTo],getTime,getMoney]
            xy_tran.append(relation)
        if (getFrom in AccM) and (getTo in AccC):
            if not getFrom in list(triH.values()):
                #如果当前to地址未加入则加入
                triH[Hc]=getFrom
                a2nH[getFrom] = Hc
                Hc+=1
            if not getTo in list(triB.values()):
                #如果当前to地址未加入则加入
                triB[Bc]=getTo
                a2nB[getTo]=Bc
                Bc+=1
            relation = [a2nH[getFrom],a2nB[getTo],getTime,getMoney]
            yz_tran.append(relation)
    
    #存储from,to地址对应编号的文件
#     new_triA = dict(zip(triA.values(), triA.keys()))
    A_keys = triA.keys()
    sorted(A_keys)
    new_triA_sort = [(key,triA[key]) for key in A_keys]
#     mkdir('data/'+casename+"/")
    #输出文件
    dict_from_path = './inputData/AML/data/' + casename + '/all-normal-tx_A.txt'
    with open(dict_from_path,'w') as f:
        f.write(str(new_triA_sort))

#     new_triH = dict(zip(triH.values(), triH.keys()))
    H_keys = triH.keys()
    sorted(H_keys)
    new_triH_sort = [(key,triH[key]) for key in H_keys]
#     mkdir('data/'+casename+"/")
    #输出文件
    dict_from_path = './inputData/AML/data/' + casename + '/all-normal-tx_H.txt'
    with open(dict_from_path,'w') as f:
        f.write(str(new_triH_sort))
        
#     new_triB = dict(zip(triB.values(), triB.keys()))
    B_keys = triB.keys()
    sorted(B_keys)
    new_triB_sort = [(key,triB[key]) for key in B_keys]
#     mkdir('data/'+casename+"/")
    #输出文件
    dict_from_path = './inputData/AML/data/' + casename + '/all-normal-tx_B.txt'
    with open(dict_from_path,'w') as f:
        f.write(str(new_triB_sort))
        
        
    print(np.shape(xy_tran))
    print(np.shape(yz_tran))
    xy_df = pd.DataFrame(xy_tran)
    yz_df = pd.DataFrame(yz_tran)
    #zy_df = pd.DataFrame()
    tmp = yz_df.loc[:,0]
    zy_df = yz_df.drop(yz_df.columns[[0]],axis=1) 
    zy_df.insert(1,0,value=tmp)
    #zy_df = pd.DataFrame(zy_tran)
    #print(xy_df,'\n',yz_df)
    print(len(triA),len(triH),len(triB))
    xy_df.to_csv('./inputData/AML/'+casename+"/all-normal-tx-cube_xy.csv",header=0,index=False)
    yz_df.to_csv('./inputData/AML/'+casename+"/all-normal-tx-cube_yz.csv",header=0,index=False)
    zy_df.to_csv('./inputData/AML/'+casename+"/all-normal-tx-cube_zy.csv",header=0,index=False)
    print('完毕')
