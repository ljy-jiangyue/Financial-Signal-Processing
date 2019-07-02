#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import xlsxwriter
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
from matplotlib import font_manager
my_font = font_manager.FontProperties(fname="/Library/Fonts/Songti.ttc")
import sys
 
sys.setrecursionlimit(1000000) 


# In[3]:


#TODO：如果是从bloomberg采集的数据请把这个设置为True，如果不是则改为False
bloomberg=True
#TODO：excel文件名
title='副本历史数据.xlsx'

if bloomberg:
    sheet='Sheet1'
    date_col="a"
    val_col="b"
    df_hisVol = pd.read_excel(title,sheet_name = sheet)
    df_hisVol=df_hisVol.drop([0,1,2,3,4,5])
    df_hisVol.columns = ['a', 'b']
else:
    #TODO：sheet名
    sheet='万得'
    #TODO：日期一列
    date_col="Unnamed: 0"
    #TODO：数据列
    val_col="全部A股"
    df_hisVol = pd.read_excel(title,sheet_name = sheet)
    #TODO：空白列的行数
    df_hisVol=df_hisVol.drop([0,880,881,882])


# In[4]:


#sns.lineplot(x="Unnamed: 0", y="全部A股",data=df_hisVol)


# In[5]:


def ensure_float(x):
    if isinstance(x,np.float):
        return x
    else :
        return 0
ensure_float(df_hisVol[date_col])
d=df_hisVol[date_col].tolist()
ttt=np.array([type(i) for i in d])
h=df_hisVol[val_col].tolist()
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.plot(np.array(d),np.array(h))
#TODO：标题
plt.title("Historical Raw Data")
#sns.scatterplot(x="Unnamed: 0", y="全部A股",data=df_hisVol)


# In[6]:


def wave_band_rec(data):
    print(data.idxmin())


# In[7]:


df_hisVol=df_hisVol.fillna(0)
global_min=df_hisVol[val_col].idxmin()
last_valid_index=df_hisVol.last_valid_index()
first_valid_index=df_hisVol.first_valid_index()
first_valid_index


# In[8]:


def local_max(data, prev_min_idx, cur_idx, cur_max_idx, flag, direc, conf):
    #print(cur_idx)
    u=1+conf/100
    d=1-(conf/100)/u
    if cur_idx>last_valid_index or cur_idx<first_valid_index:
        return
    if flag:
        top.append(cur_max_idx)
        return local_min(data, cur_max_idx, cur_max_idx, cur_max_idx, False, direc, conf)
    else:
        cur=data[cur_idx]
        maxc=data[cur_max_idx]
        prev=data[prev_min_idx]
        if cur>maxc and cur>u*prev:
            return local_max(data,prev_min_idx,cur_idx+direc,cur_idx,False, direc, conf)
        else:
            if cur<d*maxc:
                return local_max(data,prev_min_idx,cur_idx,cur_max_idx, True, direc, conf)
            else:
                return  local_max(data, prev_min_idx,cur_idx+direc,cur_max_idx, False, direc, conf)
        
def local_min(data,prev_max_idx,cur_idx,cur_min_idx,flag,direc, conf):
    u=1+conf/100
    d=1-(conf/100)/u
    if cur_idx>last_valid_index or cur_idx<first_valid_index:
        return
    if flag:
        bottom.append(cur_min_idx)
        return local_max(data, cur_min_idx, cur_min_idx, cur_min_idx, False, direc, conf)
    else:
        cur=data[cur_idx]
        minc=data[cur_min_idx]
        prev=data[prev_max_idx]
        if cur<minc and cur<d*prev:
            return local_min(data,prev_max_idx,cur_idx+direc,cur_idx,False, direc, conf)
        else:
            if cur>u*minc:
                return local_min(data,prev_max_idx,cur_idx,cur_min_idx, True, direc, conf)
            else:
                return  local_min(data, prev_max_idx,cur_idx+direc,cur_min_idx, False, direc, conf)


# In[24]:


top=[]
bottom=[]
def drawl(data, x, c):
    local_max(data, global_min, global_min, global_min, False,1,c)
    local_max(data, global_min, global_min, global_min, False,-1,c)
    #print("顶点")
    #print([x[i] for i in top])
    #print("底点")
    #print([x[i] for i in bottom])
    print(len(top))
    df_top = pd.DataFrame(data={'date':[x[i] for i in top], 'value':[data[i] for i in top]})
    df_bottom = pd.DataFrame(data={'date':[x[i] for i in bottom], 'value':[data[i] for i in bottom]})
    df_top.to_excel("output_t{coeff}.xlsx".format(coeff=c), sheet_name='Sheet_name_1') 
    df_bottom.to_excel("output_b{coeff}.xlsx".format(coeff=c), sheet_name='Sheet_name_1') 
    a=top
    a.extend(bottom)
    a.sort()
    top.sort()
    bottom.sort()
    guaidian=[data[i] for i in a]
    date=[x[i] for i in a]
    plt.title("阈值为{co}的顶点和拐点".format(co=c), fontproperties=my_font)
    sns.scatterplot(x="date", y="value",data=df_top, label="顶点")
    sns.scatterplot(x="date", y="value",data=df_bottom, label="底点")
 
    plt.plot(np.array(date), np.array(guaidian))
    plt.legend(prop=my_font)
    plt.show()
    return 
    
    


# In[25]:


drawl(df_hisVol[val_col], df_hisVol[date_col],10)


# In[16]:


top=[]
bottom=[]
drawl(df_hisVol[val_col], df_hisVol[date_col],20)


# In[17]:


top=[]
bottom=[]
drawl(df_hisVol[val_col], df_hisVol[date_col],5)


# In[26]:


title='副本c0c4a741078ee124.xlsx'
sheet='万得'
#TODO：日期一列
date_col="Unnamed: 0"
#TODO：数据列
val_col="全部A股"
df_hisVol = pd.read_excel(title,sheet_name = sheet)
#TODO：空白列的行数
df_hisVol=df_hisVol.drop([0,880,881,882])


# In[32]:


df_hisVol=df_hisVol.fillna(0)
global_min=df_hisVol[val_col].idxmin()
last_valid_index=df_hisVol.last_valid_index()
first_valid_index=df_hisVol.first_valid_index()
d=df_hisVol[date_col].tolist()
ttt=np.array([type(i) for i in d])
h=df_hisVol[val_col].tolist()
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.plot(np.array(d),np.array(h))
#TODO：标题
plt.title("Historical Raw Data")


# In[28]:


top=[]
bottom=[]
drawl(df_hisVol[val_col], df_hisVol[date_col],10)


# In[29]:


top=[]
bottom=[]
drawl(df_hisVol[val_col], df_hisVol[date_col],20)


# In[30]:


top=[]
bottom=[]
drawl(df_hisVol[val_col], df_hisVol[date_col],5)


# In[ ]:





# In[134]:





# In[ ]:





# In[ ]:




