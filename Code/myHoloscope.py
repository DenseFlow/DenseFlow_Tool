import sys
sys.path.append("F:/Inpluslab2023/2023antiML_Experiment/spartan2-master")
import spartan as st
import time
import pandas as pd
import Code.holodatatran as holo
import numpy as np



def myReadData(path):
    f = open(path, 'r')
    a = f.read()
    data = eval(a)
    f.close()
    return data
# 获得从编号->地址的映射关系。输入：原始数据的csv名称
# def num_to_addr(casename):
#     path = './inputData/AML/data/' + casename + '/all-normal-tx_from.txt'
#     dict_from = myReadData(path)
#     path = './inputData/AML/data/' + casename+ '/all-normal-tx_to.txt'
#     dict_to = myReadData(path)
#     return dict_from,dict_to

# # 获得从地址->编号的映射关系。输入：原始数据的csv名称
# def addr_to_num(csvname):
#     dict_from, dict_to = num_to_addr(csvname)
#     dict_from = np.array(dict_from)
#     dict_to = np.array(dict_to)

#     new_dict_from = dict(zip(dict_from[:,1], dict_from[:,0]))
#     new_dict_to = dict(zip(dict_to[:,1], dict_to[:,0]))
#     return new_dict_from, new_dict_to

def Search_full_tranrecord(fromnumheist,tonumheist,casename):
    #输入:from地址序号list、to地址序号list
    TR = pd.read_csv('./inputData/AML/'+casename+'/all-normal-tx_holo.csv')
    print(TR.columns)
    tr = pd.DataFrame(columns = TR.columns)
    d_f,d_t = num_to_addr(casename)
    addr_f=[]
    addr_t=[]
    for f in fromnumheist:
        addr_f.append(list(d_f[f])[1])
    for t in tonumheist:
        addr_t.append(list(d_t[t])[1])
    for af in addr_f:
#         print(af)
        af_tran = TR.loc[TR['0']==af]
#         print(af_tran)
        tr=tr.append(af_tran)
        #print(tr)
    for at in addr_t:
        at_tran = TR.loc[TR['1']==at]
        tr = tr.append(at_tran)
    return tr   

def outputheist(res,from_n2a,to_n2a):
    R = []
    C=[]
    for r in res:
        rows, cols = r[0]
        #print(rows,cols)
        # to subgraph
        for rr in rows:
            R.append(rr)
        for cc in cols:
            C.append(cc)
    add_h = []
    for rr,cc in zip(R,C):
        addtemp = list(from_n2a[rr])[1]
        if addtemp not in add_h:
            add_h.append(addtemp)
        addtemp = list(to_n2a[cc])[1]
        if addtemp not in add_h:
            add_h.append(addtemp)
    return add_h
def build_hs(casename,numSing=10):
    print('现在正在进行案件',casename,'的数据预处理...\n')
    print('读取数据')
    address = pd.read_csv(f'./inputData/AML/'+casename+'/all-normal-address.csv')
    heist = address.loc[address['label']=='heist']
    heist_address = heist['address'].tolist()
    from_a2n,to_a2n = holo.addr_to_num(casename)
    from_n2a,to_n2a = holo.num_to_addr(casename)
    filePath =  f'./inputData/AML/'+casename+'/all-normal-tx_holo.csv'
    print('处理数据')
    tensor_data = st.loadTensor(path = filePath, header=None)
    #格式
    tensor_data.data = tensor_data.data.drop(columns=[0])
    tensor_data.data =tensor_data.data.drop([0])
    tensor_data.data.columns=[0,1,2,3,4]
    tensor_data.data[2] = tensor_data.data[2].str.replace('/','-')
    stensor = tensor_data.toSTensor(hasvalue=True, mappers={2:st.TimeMapper(timeformat='%Y-%m-%d')})
    graph = st.Graph(stensor, bipartite=True, weighted=True, modet=2)
    hs = st.HoloScope(graph,numSing=numSing)
    print(casename,'数据构造完毕')
    return hs

def output_holo(casename,k,hs):
    t = time.time()
    res = hs.run(level=0, k=k)
    res1 = hs.run(level=1, k=k)
    res2 = hs.run(level=2, k=k)
    res3 = hs.run(level=3, k=k)
    res4 = hs.run(level=4, k=k)
    res5 = hs.run(level=5, k=k)
    res6 = hs.run(level=6, k=k)
    print(casename,' k=',k,'7种运行总耗时：')
    print(f'cost:{time.time() - t:.8f}s namely:{((time.time() - t)/60):.8f}min')
    from_a2n,to_a2n = holo.addr_to_num(casename)
    from_n2a,to_n2a = holo.num_to_addr(casename)
    add_h = outputheist(res,from_n2a,to_n2a)
    add_h1 = outputheist(res1,from_n2a,to_n2a)
    add_h2 = outputheist(res2,from_n2a,to_n2a)
    add_h3 = outputheist(res3,from_n2a,to_n2a)
    add_h4 = outputheist(res4,from_n2a,to_n2a)
    add_h5 = outputheist(res5,from_n2a,to_n2a)
    add_h6 = outputheist(res6,from_n2a,to_n2a)
    print('heist数量计算结果：',len(add_h),len(add_h1),len(add_h2),len(add_h3),len(add_h4),len(add_h5),len(add_h6))
    print('结果存储ing')
    a = pd.DataFrame(add_h,columns=['heist0'])
    a1 = pd.DataFrame(add_h1,columns=['heist1'])
    a2 = pd.DataFrame(add_h2,columns=['heist2'])
    a3 = pd.DataFrame(add_h3,columns=['heist3'])
    a4 = pd.DataFrame(add_h4,columns=['heist4'])
    a5 = pd.DataFrame(add_h5,columns=['heist5'])
    a6 = pd.DataFrame(add_h6,columns=['heist6'])
    writer = pd.ExcelWriter(f'./inputData/AML/'+casename+'/myheist_k_'+str(k)+'.xlsx')
    a.to_excel(writer,'Sheet0')
    a1.to_excel(writer,'Sheet1')
    a2.to_excel(writer,'Sheet2')
    a3.to_excel(writer,'Sheet3')
    a4.to_excel(writer,'Sheet4')
    a5.to_excel(writer,'Sheet5')
    a6.to_excel(writer,'Sheet6')
    writer.save()
    writer.close()