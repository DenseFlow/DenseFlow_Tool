from Code.info import *
import spartan as st
import Code.Datatran_1 as dt
import Code.Cubedatatran as cube
import Code.holodatatran as holo
import os
import pandas as pd
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print( "new folder")
    else:
        print("There is this folder")
def fraudar(casename):
    filePath =  f'./inputData/AML/'+casename+'/all-normal-tx_fraudar.csv'# Remember to add spartan to you PATH

    # load graph data
    tensor = st.loadTensor(path = filePath)

    stensor = tensor.toSTensor(hasvalue=False)
    fd = st.Fraudar(stensor)
    # run the model
    out_path = "./Fraudar_output/"
    file_name = casename+"_out/"
    mkdir(out_path+file_name)
    res = fd.run(k=10, out_path = "./Fraudar_output/", file_name = casename+"_out/" ,maxsize=[100, 100])
    dt.fraud_tran(casename)
    print('完成fraudar结果转换与存储')

def cubeflow(casename):    
    print("案件",casename,'\n')
    xy_path = f'./inputData/AML'+'/'+casename+"/all-normal-tx-cube_xy.csv"
    zy_path = f'./inputData/AML'+'/'+casename+"/all-normal-tx-cube_zy.csv"
    #gt_path = f'./inputData/CFD-{dim}/gt.npy'

    out_path = "./CubeFlow_output/"+casename+"_out/"
    file_name = casename+"_cubeflow.txt"

    outpath = out_path+file_name # '': not save results
    mkdir(out_path)

    amt_tensor = st.loadTensor(path=xy_path, header=None)
    cmt_tensor = st.loadTensor(path=zy_path, header=None)

    amt_stensor = amt_tensor.toSTensor(hasvalue=True)
    cmt_stensor = cmt_tensor.toSTensor(hasvalue=True)
    # maxshape = max(amt_stensor.shape[1], cmt_stensor.shape[0])
    # amt_stensor.shape = (amt_stensor.shape[0], maxshape)
    # cmt_stensor.shape = (maxshape, cmt_stensor.shape[1])
    #print(amt_stensor.shape)
    #print(cmt_stensor.shape)

    cf = st.CubeFlow([amt_stensor, cmt_stensor], alpha=0.2, k=10, dim=3, outpath=outpath)

    res = cf.run(del_type=1, maxsize=-1)
    print("案件",casename,'完成cubeflow\n')
    n2aA,n2aH,n2aB = cube.num_to_addr(casename)
    print(len(n2aA),len(n2aH),len(n2aB))
    cube_heist = []
    for num in res[0][0][0]:
        cube_heist.append(n2aA[num][1])
    for num in res[0][0][1]:
        cube_heist.append(n2aH[num][1])
    for num in res[0][0][2]:
        cube_heist.append(n2aB[num][1])
    a1 = pd.DataFrame(cube_heist,columns=['heist'])
    path = './CubeFlow_output/'+casename+"_out/"
    file_name = casename+"_cubehseit.csv"
    outpath = out_path+file_name # '': not save results
    mkdir(out_path)
    #print(a1)
    a1.to_csv(outpath,index=False)
    print("案件",casename,'完成cubeflow存储\n')

def holoscope(casename,k,level):
    print(casename)
    filePath =  f'./inputData/AML/'+casename+'/all-normal-tx_holo.csv'
    tensor_data = st.loadTensor(path = filePath, header=None)
    #格式
    tensor_data.data = tensor_data.data.drop(columns=[0])
    tensor_data.data =tensor_data.data.drop([0])
    tensor_data.data.columns=[0,1,2,3,4]
    tensor_data.data[2] = tensor_data.data[2].str.replace('/','-')
    stensor = tensor_data.toSTensor(hasvalue=True, mappers={2:st.TimeMapper(timeformat='%Y-%m-%d')})
    graph = st.Graph(stensor, bipartite=True, weighted=True, modet=2)
    hs = st.HoloScope(graph,numSing = 10)
    level = 1
    res = hs.run(level=level, k=10)
    from_n2a,to_n2a = holo.num_to_addr(casename)
    add_h_1 = []
    R1 = []
    C1=[]
    for r in res:
        rows, cols = r[0]
        print(rows,cols)
        # to subgraph
        for rr in rows:
            R1.append(rr)
            addtemp = list(from_n2a[rr])[1]
            if addtemp not in add_h_1:
                add_h_1.append(addtemp)
        for cc in cols:
            C1.append(cc)
            addtemp = list(to_n2a[cc])[1]
            if addtemp not in add_h_1:
                add_h_1.append(addtemp)   

    a1 = pd.DataFrame(add_h_1,columns=['heist1'])
    out_path = './Holoscope_output/'+casename+"_out/"
    file_name = casename+"_hs_level_"+str(level)+".csv"
    outpath = out_path+file_name # '': not save results
    mkdir(out_path)
    a1.to_csv(outpath,index=False)
    print('Holoscope完成')
