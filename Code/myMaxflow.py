from ortools.graph.python import max_flow
import pandas as pd
import os
import numpy as np
from treelib import Tree


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print( "new folder")
    else:
        print("There is this folder")
        
def build_g(casename):
    #构建图，输入案件名字，存储并输出交易节点对（startnodes和endnodes）capacities容量对应为交易金额，nodenum字典记录节点地址与数字的转换
    datatu=pd.read_csv(f'./inputData/AML/'+casename+'/all-normal-tx.csv')
    row = datatu.iloc[:, 0].size
    nodelist = []
    nodenum = {}
    number=0
    start_nodes = []
    end_nodes = []
    capacities = []
    print('构造图ing')
    #遍历交易
    for i in range(row):
        #构建节点列表：
        addf = datatu.iloc[i, 1]
        addt = datatu.iloc[i, 2]
        #如果当前地址未加入图中：
        if addf not in nodelist:
            nodelist.append(addf)
            number+=1
            nodenum[addf]=number

        if addt not in nodelist:
            nodelist.append(addt)
            number+=1
            nodenum[addt]=number

        money = float(datatu.iloc[i,3])*1e-18
        #筛选部分交易
        if datatu.loc[i,'isError']== 0:
            #print('from',addf,':',nodenum[addf],'to',addt,':',nodenum[addt],money)
            if(nodenum[addf]!=nodenum[addt] and money != 0.0):
                #不考虑自己转给自己的，不考虑资金为0的交易【不加入到交易图中】
                start_nodes.append(nodenum[addf])
                end_nodes.append(nodenum[addt])
                capacities.append(money)

    start_nodes = np.array(start_nodes)
    end_nodes = np.array(end_nodes)
    capacities = np.array(capacities)
    """From Taha 'Introduction to Operations Research', example 6.4-2."""
    nodeadd = {k:v for v,k in nodenum.items()}
    print("完成构建图，节点数：", number,"边数：", len(capacities))
    gpath = './Maxflow_graph/'+casename+'/'
    mkdir(gpath)
    np.save(gpath+'start_nodes.npy',start_nodes)
    np.save(gpath+'end_nodes.npy',end_nodes)
    np.save(gpath+'capacities.npy',capacities)
    np.save(gpath+'nodenum.npy',nodenum)
    return start_nodes,end_nodes,capacities,nodenum

def read_g(casename):
    #读取已存储的图
    print('已完成构建，读取图ing')
    gpath = './Maxflow_graph/'+casename+'/'
    start_nodes=np.load(gpath+'start_nodes.npy')
    start_nodes=start_nodes.tolist()
    end_nodes=np.load(gpath+'end_nodes.npy')
    end_nodes=end_nodes.tolist()
    capacities=np.load(gpath+'capacities.npy')
    capacities=capacities.tolist()
    nodenum = np.load(gpath+'nodenum.npy', allow_pickle=True).item()
    print('读取完成')
    return start_nodes,end_nodes,capacities,nodenum

#source = nodenum[sourceadds[0]]

def find_s_t(t,s,start_nodes,end_nodes,capacities,p=True):
    #输入图，终点节点t与源节点s，start_nodes,end_nodes,capacities为构建好的图数据，p控制print
    """MaxFlow simple interface example."""
    # Instantiate a SimpleMaxFlow solver.
    smf = max_flow.SimpleMaxFlow()
    #调用库函数
    # Define three parallel arrays: start_nodes, end_nodes, and the capacities
    # between each pair. For instance, the arc from node 0 to node 1 has a
    # capacity of 20.
    

    # Add arcs in bulk.
    #   note: we could have used add_arc_with_capacity(start, end, capacity)
    all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

    # Find the maximum flow between node 0 and node 4.
    status = smf.solve(s, t)

    if status != smf.OPTIMAL:
        print('There was an issue with the max flow input.')
        print(f'Status: {status}')
        return [1,smf.optimal_flow(),-3]
    if(smf.optimal_flow()!=0):
        level=0#看一下source到当前节点的交易数？这个是最初写的，现在其实没有用到这个level，可以无视
        #print('source节点number',s)
        if p:#p为真时进行输出，否则不输出最大流情况
            print('Max flow:', smf.optimal_flow())
            print('')
            print(' Arc    Flow / Capacity')
        solution_flows = smf.flows(all_arcs)
        #flowadd = []
        for arc, flow, capacity in zip(all_arcs, solution_flows, capacities):
            if flow !=0:#只看不为0的flow
                if p:
                    print(f'{smf.tail(arc)} / {smf.head(arc)}   {flow:3}  / {capacity:3}')
                level+=1
        #print('Source side min-cut:', smf.get_source_side_min_cut())
        #print('Sink side min-cut:', smf.get_sink_side_min_cut())
        
#             addtmp = nodeadd[smf.tail(arc)]
#             if addtmp not in flowadd:
#                 flowadd.append(addtmp)
#                 #print(type(addtmp))
#             addtmp = nodeadd[smf.head(arc)]
#             if addtmp not in flowadd:
#                 flowadd.append(addtmp)
        return [1,smf.optimal_flow(),level]
    else:
        #print('最大流0')
        return [0,0,0]
    
def find_s_t_address(t,s,start_nodes,end_nodes,capacities):
    """MaxFlow simple interface example."""
    #与上面类似的一个函数，不同的是这里面会存储流链路中的地址
    # Instantiate a SimpleMaxFlow solver.
    smf = max_flow.SimpleMaxFlow()

    # Define three parallel arrays: start_nodes, end_nodes, and the capacities
    # between each pair. For instance, the arc from node 0 to node 1 has a
    # capacity of 20.
    
    
    # Add arcs in bulk.
    #   note: we could have used add_arc_with_capacity(start, end, capacity)
    all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

    # Find the maximum flow between node 0 and node 4.
    status = smf.solve(s, t)
    flownum = []
    if status != smf.OPTIMAL:
        print('There was an issue with the max flow input.')
        print(f'Status: {status}')
        return flownum
    
    if(smf.optimal_flow()!=0):
        level=0#看一下source到当前节点的层数？
        #print('Max flow:', smf.optimal_flow())
       # print('')
        #print(' Arc    Flow / Capacity')
        solution_flows = smf.flows(all_arcs)
        
        for arc, flow, capacity in zip(all_arcs, solution_flows, capacities):
            if flow !=0:#只看不为0的flow
                #print(f'{smf.tail(arc)} / {smf.head(arc)}   {flow:3}  / {capacity:3}')
                if smf.tail(arc) not in flownum:
                    flownum.append(smf.tail(arc))
                if smf.head(arc) not in flownum:
                    flownum.append(smf.head(arc))
                
                #print(nodeadd[smf.tail(arc)],'——》',nodeadd[smf.head(arc)])
                level+=1
#         print('Source side min-cut:', smf.get_source_side_min_cut())
#         print('Sink side min-cut:', smf.get_sink_side_min_cut())
        
            #print("当前",len(flowadd))
        return flownum
    else:
        #print('最大流0')
        return flownum
    
def output_flow_add(casename,k,level,sourceadd,Show = False, Save = True):
    #input:案件casename+level+k
    #1.outputhesit结果文件
    
    print('当前正在运行：',casename,'k=',k,'level=',level)
    print('读取对应heist地址...')
    heist1 = pd.read_excel(f'./inputData/AML/'+casename+'/myheist_k_'+str(k)+'.xlsx',sheet_name='Sheet'+str(level),index_col=0)
    heist1 = heist1.iloc[:,0].tolist()
    node_heist1 = [] 
    start_nodes,end_nodes,capacities,nodenum = read_g(casename)
    source = nodenum[sourceadd]
    for add in heist1:
        node_heist1.append(nodenum[add])
    print('进行最大流算法...')
    i=0
    #非零的最大流？
    flowadd = []
    flownums = []

    nonzeroflow = 0
    flowvalue = []
    levels = []
    
    for node_h in node_heist1:
        #print(i,':','source：',source,'到当前节点',node_h,'最大流算法：')
        #计算地址
        flownum = find_s_t_address(node_h,source,start_nodes,end_nodes,capacities)
        flownums.extend(flownum)
        #计算流值
        result = find_s_t(node_h,source,start_nodes,end_nodes,capacities,p=Show)
        if(result[1]>0):
            nonzeroflow+=result[0]
            flowvalue.append(result[1])
            levels.append(result[2])

        i+=1
    print('共',len(flowvalue),'条非0流，总流值：',sum(flowvalue))   
    flownums = list(set(flownums))
    len(flownums)
    flowadd = []
    nodeadd = {k:v for v,k in nodenum.items()}
    for num in flownums:
        flowadd.append(nodeadd[num])

    total_heist = list(set(flowadd+heist1))
    holoouput = pd.DataFrame(heist1,columns=['holo_heist'])
    flowouput = pd.DataFrame(flowadd,columns=['flow_heist'])
    totalouput = pd.DataFrame(total_heist,columns=['all_heist'])
    if Save:
        print('地址存储中...')
        out_path ='F:/Inpluslab2023/2023antiML_Experiment/spartan2-tutorials-master/spartan2-tutorials-master/Result/'+casename+"_out/"

        mkdir(out_path)
        writer = pd.ExcelWriter(out_path+casename+'_k_'+str(k)+'_level_'+str(level)+'.xlsx')

        holoouput.to_excel(writer,'Sheet1')
        flowouput.to_excel(writer,'Sheet2')
        totalouput .to_excel(writer,'Sheet3')
        writer.save()
        writer.close()
    return(flowvalue)

def find_whole_flow(t,s,start_nodes, end_nodes, capacities,p=True):
    """MaxFlow simple interface example."""
    # Instantiate a SimpleMaxFlow solver.
    #方便最大流可视化的函数，输出一条进行合并处理过的最大流，
    smf = max_flow.SimpleMaxFlow()

    # Define three parallel arrays: start_nodes, end_nodes, and the capacities
    # between each pair. For instance, the arc from node 0 to node 1 has a
    # capacity of 20.
    

    # Add arcs in bulk.
    #   note: we could have used add_arc_with_capacity(start, end, capacity)
    all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

    # Find the maximum flow between node 0 and node 4.
    status = smf.solve(s, t)

    if status != smf.OPTIMAL:
        print('There was an issue with the max flow input.')
        print(f'Status: {status}')
        return {}
    wholeflow = {}
    if status != smf.OPTIMAL:
        print('There was an issue with the max flow input.')
        print(f'Status: {status}')
        #return [1,smf.optimal_flow(),-3]
    if(smf.optimal_flow()!=0):
        level=0#看一下source到当前节点的交易数？
        print('source节点number',s)
        if p:
            print('Max flow:', smf.optimal_flow())
            print('')
            print(' Arc    Flow / Capacity')
        solution_flows = smf.flows(all_arcs)

        print(type(solution_flows),np.shape(solution_flows))
        #flowadd = []
        for arc, flow, capacity in zip(all_arcs, solution_flows, capacities):

            if flow !=0:#只看不为0的flow
                if p:
                    print(f'{smf.tail(arc)} / {smf.head(arc)}   {flow:3}  / {capacity:3}')
                if (smf.tail(arc),smf.head(arc)) in list(wholeflow.keys()):
                    wholeflow[(smf.tail(arc),smf.head(arc))] += flow
                else:
                    wholeflow[(smf.tail(arc),smf.head(arc))] = flow
                level+=1
        #print('Source side min-cut:', smf.get_source_side_min_cut())
        #print('Sink side min-cut:', smf.get_sink_side_min_cut())

    #             addtmp = nodeadd[smf.tail(arc)]
    #             if addtmp not in flowadd:
    #                 flowadd.append(addtmp)
    #                 #print(type(addtmp))
    #             addtmp = nodeadd[smf.head(arc)]
    #             if addtmp not in flowadd:
    #                 flowadd.append(addtmp)
    return wholeflow
