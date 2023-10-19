import sys
sys.path.append("F:/Inpluslab2023/2023antiML_Experiment/spartan2-master")
import spartan as st
import os
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print( "new folder")
    else:
        print("There is this folder")
        
import numpy as np
import pandas as pd
import os
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

# csvtodata(csv_path)    将原始csv里的from\to地址转化编号，并存储映射关系。输入：csv路径
# myReadData(path)       读取单个映射关系文件。输入：文件路径
# num_to_addr(csvname)   获得从编号->地址的映射关系。输入：原始数据的csv名称
# addr_to_num(csvname)   获得从地址->编号的映射关系。输入：原始数据的csv名称

# saveaddr(csvname,ifrows,data)   保存运算结果的实际地址。输入：原始数据的csv名称、是否为行、子集的编号
# 使用方法：saveaddr(csvname,1,lwRes[0][0])
#         saveaddr(csvname,0,lwRes[0][1])

# 将原始csv里的from\to地址转化编号，并存储映射关系。输入：csv路径
# 思路：设置两个字典from字典、to字典，存储键值
def csvtodata(casename):
    #csv_path = 'all_tx_easyfihack.csv'
    csv_path ='./inputData/AML/'+casename+"/all-normal-tx.csv"
    raw_data = pd.read_csv(csv_path)
    # 获取from的地址
    dict_from = {}
    dict_to = {}
    relation = []
    count_from = 0
    count_to = 0
    # line[2]是from line[3]是to
    print('读取交易完成\n')
    datasetoverview(casename)
    print('构建序号地址映射')
    for idx,data in raw_data.iterrows():
        #只记录交易金额非0的交易
        if data['value'] == 0.0:
             continue
        getFrom = data['from']
        getTo = data['to']
        # 构建from和序号的映射
        if not getFrom in dict_from:
            dict_from[getFrom] = count_from
            count_from = count_from + 1
        # 构建to和序号的映射
        if not getTo in dict_to:
            dict_to[getTo] = count_to
            count_to = count_to + 1
        # 找到对应的数字
        relation.append([dict_from[getFrom],dict_to[getTo]])
    print('完成构建序号地址映射')
    # 排序
    relation.sort()
    # 去重,relation_new为去重后的关系列表
    relation_new = []
    relation_new.append(relation[0])
    new_count = 1
    #去重
    for i in relation:
        if i != relation_new[new_count - 1]:
            relation_new.append(i)
            new_count = new_count + 1

    #不要去重，统计边数
    relation_count = []
    relation_count = pd.value_counts(relation)
    #dict_from = sorted(dict_from.items(),key = lambda x:x[1])
    #dict_to = sorted(dict_to.items(),key = lambda x:x[1])
    print('存储numadd关系文件...\n')
    #存储from,to地址对应编号的文件
    new_dict_from = dict(zip(dict_from.values(), dict_from.keys()))
    from_keys = new_dict_from.keys()
    sorted(from_keys)
    new_dict_from_sort = [(key,new_dict_from[key]) for key in from_keys]
    mkdir('data/'+casename+"/")
    #输出from文件
    dict_from_path = './inputData/AML/data/' + casename + '/all-normal-tx_from.txt'
    with open(dict_from_path,'w') as f:
        f.write(str(new_dict_from_sort))

    #to的
    new_dict_to = dict(zip(dict_to.values(), dict_to.keys()))
    to_keys = new_dict_to.keys()
    sorted(to_keys)
    new_dict_to_sort = [(key, new_dict_to[key]) for key in to_keys]
    # 输出to文件
    dict_to_path = './inputData/AML/data/' + casename + '/all-normal-tx_to.txt'
    with open(dict_to_path, 'w') as f:
        f.write(str(new_dict_to_sort))

    #输出关系文件，调整输出格式
    
    edgef = []
    edget = []
    edgenum = []
    print('count',relation_count)
    for d,v in relation_count.items():
#         print(d,',',v)
        edgef.append(d[0])
        edget.append(d[1])
        edgenum.append(v)
    relationship = {'edgef':edgef,'edget':edget}
    relationship_df = pd.DataFrame.from_dict(relationship)
#     print(relationship)
#     print(relationship_df)
    relationship_df.to_csv('./inputData/AML/'+casename+'/all-normal-tx_fraudar.csv',header=0,index=False)
    txtname = './inputData/AML/data/' + casename + '/all-normal-tx'+ 'count.txt'
    with open(txtname,'w') as f:
        for i in relation:
            f.write(str(i[0]) + ' '+ str(i[1]) + '\n')

# 读取单个映射关系文件。输入：文件路径
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
def addr_to_num(csvname):
    dict_from, dict_to = num_to_addr(csvname)
    dict_from = np.array(dict_from)
    dict_to = np.array(dict_to)

    new_dict_from = dict(zip(dict_from[:,1], dict_from[:,0]))
    new_dict_to = dict(zip(dict_to[:,1], dict_to[:,0]))
    return new_dict_from, new_dict_to

# 保存运算结果的实际地址。输入：原始数据的csv名称、是否为行、子集的编号
def saveaddr(csvname,ifrows,data):
    #输出结果
    dict_from, dict_to = num_to_addr(csvname)
    path = 'out/' + csvname + '_result'

    if ifrows:
        path = path + '_rows.txt'
        f = open(path, 'w')
        for i in data:
            f.write(str(dict_from[i]) + '\n')
        f.close()
    else:
        path = path + '_cols.txt'
        f = open(path, 'w')
        for i in data:
            f.write(str(dict_to[i]) + '\n')
        f.close()

# 根据已知标签设置点权重。输入：原始数据的csv名称、可疑节点所在csv、设置的权重
# 权重结果保存到susp.cols和susp.rows

def fraud_tran(casename):

    print(casename)
    out_path = "./Fraudar_output/"
    file_name = casename+"_out/"

    from_n2a,to_n2a = num_to_addr(casename)
    #read txt method three
    frow = open(out_path+file_name+'_0.rows',"r")
    fcol = open(out_path+file_name+'_0.cols',"r")
    linecols = fcol.readlines()
    linerows = frow.readlines()
    numcol = []
    numrow = []
    for line in linecols:
        numcol.append(int(line))
        print (int(line))
    for line in linerows:
        numrow.append(int(line))
        print (int(line))
    addcol = []
    addrow = []
    for col,row in zip(numcol,numrow):
        rowadd = from_n2a[row]
        coladd = to_n2a[col] 
        addcol.append(list(coladd)[1])
        addrow.append(list(rowadd)[1])
    a2 = pd.DataFrame(addcol,columns=['to_heist'])
    a1 = pd.DataFrame(addrow,columns=['from_heist'])
    a3 = pd.DataFrame(addcol+addrow,columns=['all_heist'])
    #print(len(a3))
    a3.drop_duplicates()
    #print(len(addheist))
    writer = pd.ExcelWriter(out_path+file_name+'fraudar_heist.xlsx')
    a1.to_excel(writer,'Sheet1')
    a2.to_excel(writer,'Sheet2')
    a3.to_excel(writer,'Sheet3')
    writer.save()
    writer.close()
    
import pandas as pd
import time
#conding=utf8  

#test
def datasetoverview(casename):
    csv_path = './inputData/AML/'+casename+'/all-normal-tx.csv'
    raw_data = pd.read_csv(csv_path) 
    raw_data[['value']] = raw_data[['value']].astype(float)
    raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)
    heist = pd.read_csv('./inputData/AML/'+casename+'/accounts-hacker.csv')
    heist = heist[heist['label']=='heist']['address'].tolist()
    account_from = raw_data['from'].tolist()
    account_to = raw_data['to'].tolist()
    account_total = BING(account_from,account_to)
    tol_value = float(raw_data['value'].sum())*1e-18
    tmx = max(raw_data['timeStamp'])
    tmn = min(raw_data['timeStamp'])
    tres = (tmx-tmn)/(60*60*24)
    timeArray = time.localtime(tmx)
    tmx = time.strftime("%Y.%m.%d", timeArray)
    timeArray = time.localtime(tmn)
    tmn = time.strftime("%Y.%m.%d", timeArray)
    print(casename,'数据集描述：\n总账户数',len(account_total),'\n总交易数:',len(raw_data),'\n总heist数:',len(heist),'\n总交易金额:',tol_value,
          '\n时间跨度:',tmn,'-',tmx,',持续时长',tres,'（天）')