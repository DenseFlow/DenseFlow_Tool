#conding=utf8  
import os 
import pandas as pd
from Code.info import *
def CASEJIANCE(casename,k):
    out_path ='F:/Inpluslab2023/2023antiML_Experiment/spartan2-tutorials-master/spartan2-tutorials-master/Result/'+casename+"_out/"
    P = []
    R = []
    for level in range(4):
        file_path=out_path+casename+'_k_'+str(k)+'_level_'+str(level)+'.xlsx'
        folder = os.path.exists(file_path)
        if not folder:
            print("缺少结果文件",casename+'_k_'+str(k)+'_level_'+str(level))
            pre=-1
            rec=-1
        else:
            result = pd.read_excel(file_path,sheet_name = 'Sheet3')
            result = result['all_heist'].tolist()
            folder = os.path.exists(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
            if not folder:
                print("error，缺少文件")
            else:
                address = pd.read_csv(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
            heist = address.loc[address['label']=='heist']
            heist_address = heist['address'].tolist()
            correct = []
            for fh in result:
                if fh in heist_address:
                    correct.append(fh)
            if len(result)!=0:
                pre = len(correct)/len(result)
            else:
                pre = -2
            rec = len(correct)/len(heist_address)
            print(casename,':'+"\n holo+maxflow ",'(level='+str(level),'k='+str(k)+')','总共找出：',len(result),
                  '找出正确的：(heist)',len(correct),
                  "，\n正确率(Precision):",pre,
                  ',\n召回率（Recall）：',rec,'\n\n')
        P.append(pre)
        R.append(rec)
    caseresult = {'precision':P,'recall':R}
    return caseresult

def TUANHUOJIANCE(cases,k):
    RESULT = {}
    for casename in cases:
        out_path ='F:/Inpluslab2023/2023antiML_Experiment/spartan2-tutorials-master/spartan2-tutorials-master/Result/'+casename+"_out/"
        P = []
        R = []
        for level in range(4):
            file_path=out_path+casename+'_k_'+str(k)+'_level_'+str(level)+'.xlsx'
            folder = os.path.exists(file_path)
            if not folder:
                print("缺少结果文件",casename+'_k_'+str(k)+'_level_'+str(level))
                pre=-1
                rec=-1
            else:
                result = pd.read_excel(file_path,sheet_name = 'Sheet3')
                result = result['all_heist'].tolist()
                folder = os.path.exists(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
                if not folder:
                    print("error，缺少文件")
                else:
                    address = pd.read_csv(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
                heist = address.loc[address['label']=='heist']
                heist_address = heist['address'].tolist()
                correct = []
                for fh in result:
                    if fh in heist_address:
                        correct.append(fh)
                if len(result)!=0:
                    pre = len(correct)/len(result)
                else:
                    pre = -2
                rec = len(correct)/len(heist_address)
                print(casename,':'+"\n holo+maxflow ",'(level='+str(level),'k='+str(k)+')','总共找出：',len(result),
                      '找出正确的：(heist)',len(correct),
                      "，\n正确率(Precision):",pre,
                      ',\n召回率（Recall）：',rec,'\n\n')
            P.append(pre)
            R.append(rec)
        caseresult = {'precision':P,'recall':R}
        RESULT[casename]=  caseresult
    res_df=pd.DataFrame.from_dict(RESULT,orient='index')
    pre_df = res_df['precision'].apply(lambda x: pd.Series(x))
    pre_df.columns = ['precision_level_{}'.format(i) for i in range(4)]
    res_df = pd.concat([res_df, pre_df], axis=1)
    rec_df = res_df['recall'].apply(lambda x: pd.Series(x))
    rec_df.columns = ['recall_level_{}'.format(i) for i in range(4)]
    res_df = pd.concat([res_df, rec_df], axis=1)
    res_df = res_df.drop(columns=['precision','recall'])
    return res_df


def check_metrics(casename,level=1,k=10):

    PRE={}
    MC={}
    nodenum = {}
    METRICS = {}
    folder = os.path.exists(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
    if not folder:
        print(casename,"!error，缺少标签文件")
        return METRICS
    else:
        address = pd.read_csv(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
    heist = address.loc[address['label']=='heist']
    heist_address = heist['address'].tolist()
    PATH='./'
    out_path =PATH+ 'Result/'+casename+"_out/"
    myfile = casename+'_k_'+str(k)+'_level_'+str(level)+'.xlsx'
    Cube_out =PATH + 'CubeFLow_output/'+casename+"_out/"
    cubefile = casename+'_cubehseit.csv'
    Frau_out =PATH + 'Fraudar_output/'+casename+"_out/"
    fraufile = 'fraudar_heist.xlsx'
    Holo_out = PATH + 'Holoscope_output/'+casename+"_out/"
    holofile = casename+'_hs_level_1.csv'
    
    out_paths = [Frau_out+fraufile,Cube_out+cubefile,Holo_out+holofile,out_path+myfile]  
    #print(out_paths)
    for file_path in out_paths:
        #print(file_path)    
        folder = os.path.exists(file_path)
        if not folder:
            print("缺少结果文件",file_path)
            continue
        if file_path[-3:] =='csv':
            result = pd.read_csv(file_path)
            if 'cube' in file_path:
                result = result['heist'].tolist()
            else:
                result = result['heist1'].tolist()
        elif file_path[-4:]=='xlsx':
            result = pd.read_excel(file_path,sheet_name = 'Sheet3')
            result = result['all_heist'].tolist()
        correct = []
        for fh in result:
            if fh in heist_address:
                correct.append(fh)
        if len(result)!=0:
            pre = len(correct)/len(result)
        else:
            pre = -2
        rec = len(correct)/len(heist_address)
        print(casename,':')
        if 'fraudar' in file_path:
            method = 'Fraudar'
            print("\n"+method)
        elif 'cube' in file_path:
            method = 'Cubeflow'
            print("\n"+method)
        elif 'Holoscope' in file_path:
            method = 'Holoscope'
            print("\n"+method,'(level='+str(1),'k='+str(10)+')',)
        else:
            method = 'HOLO+MAXFLOW'
            print("\n"+method,'(level='+str(level),'k='+str(k)+')',)
        print('总共找出：',len(result),
              '找出正确的：(heist)',len(correct),
              "，\n正确率(Precision):",pre,
              ',\n召回率（Recall）：',rec,'\n\n')
        csv_path = './inputData/AML/'+casename+'/all-normal-tx.csv'
        raw_data = pd.read_csv(csv_path)
        raw_data[['value']] = raw_data[['value']].astype(float)
        raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)
        account = raw_data['from'].tolist() + raw_data['to'].tolist()
        account = list(set(account))
        fromisheist = raw_data[raw_data['from'].isin(result)]
        fromisheisttrue = raw_data[raw_data['from'].isin(heist_address)]


        m1 = fromisheist['value'].sum()*1e-18 #发起方主动
        m2 = fromisheisttrue['value'].sum()*1e-18

        PRE[method] = pre
        MC[method] = m1/m2
        print('追踪金额：',m1,'涉案金额：',m2,'资金覆盖率:',m1/m2)
        if m1/m2>1:
            MC[method] = 1
        else:
            MC[method] = m1/m2
        nodenum[method] =  len(result)
        print('账户总数：',len(account),'检测heist：',len(result))
        jz1 = m2/len(account)
        jz2 = m1/len(result)
        #print('相对紧致程度：','数据集紧致：',jz1,'结果紧致:',jz2,'相对紧致程度：',jz1/jz2)
        #METRICS[method] = [pre,m1/m2,len(result),jz1/jz2,1-len(result)/len(account)]
        METRICS[method] = [pre,m1/m2,len(result)]
    return METRICS

def check_metrics_my(casename,level=1,k=10):

    PRE={}
    MC={}
    nodenum = {}
    METRICS = {}
    folder = os.path.exists(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
    if not folder:
        print(casename,"!error，缺少标签文件")
        return METRICS
    else:
        address = pd.read_csv(f'./inputData/AML/'+casename+'/accounts-hacker.csv')
    heist = address.loc[address['label']=='heist']
    heist_address = heist['address'].tolist()
    PATH='./'
    out_path =PATH+ 'Result/'+casename+"_out/"
    myfile = casename+'_k_'+str(k)+'_level_'+str(level)+'.xlsx'
    file_path = out_path+myfile
    result = pd.read_excel(file_path,sheet_name = 'Sheet3')
    result = result['all_heist'].tolist()
    correct = []
    for fh in result:
        if fh in heist_address:
            correct.append(fh)
    if len(result)!=0:
        pre = len(correct)/len(result)
    else:
        pre = -2
    rec = len(correct)/len(heist_address)
    method = 'HOLO+MAXFLOW'
    print("\n"+method,'(level='+str(level),'k='+str(k)+')',)
    print('总共找出：',len(result),
          '找出正确的：(heist)',len(correct),
          "，\n正确率(Precision):",pre,
          ',\n召回率（Recall）：',rec,'\n\n')
    csv_path = './inputData/AML/'+casename+'/all-normal-tx.csv'
    raw_data = pd.read_csv(csv_path)
    raw_data[['value']] = raw_data[['value']].astype(float)
    raw_data[['timeStamp']] = raw_data[['timeStamp']].astype(int)
    account = raw_data['from'].tolist() + raw_data['to'].tolist()
    account = list(set(account))
    fromisheist = raw_data[raw_data['from'].isin(result)]
    fromisheisttrue = raw_data[raw_data['from'].isin(heist_address)]
    m1 = fromisheist['value'].sum()*1e-18 #发起方主动
    m2 = fromisheisttrue['value'].sum()*1e-18
    mrc=min(m1/m2,1)
    print('追踪金额：',m1,'涉案金额：',m2,'资金覆盖率:',mrc)
    print('账户总数：',len(account),'检测heist：',len(result))
    jz1 = m2/len(account)
    jz2 = m1/len(result)
    #print('相对紧致程度：','数据集紧致：',jz1,'结果紧致:',jz2,'相对紧致程度：',jz1/jz2)
    #METRICS[method] = [pre,m1/m2,len(result),jz1/jz2,1-len(result)/len(account)]
    METRICS[method] = [pre,m1/m2,len(result)]
    return METRICS