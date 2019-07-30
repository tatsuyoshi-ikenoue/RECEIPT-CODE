#!/usr/bin/env python
# coding: utf-8

# # IMPORT DATA

# In[1]:


import pandas as pd
import numpy  as np
import os
import sys
import re


# In[2]:


import zenhan
from numpy import vectorize
import pdread
import DokenPo_insurance


# In[3]:


def to_float(x):
    x = str(x).replace('L', '')
    x = str(x).replace('H', '')
    try: return float(x)
    except: return np.nan


# ## IMPORT CKD LIST

# In[4]:


# ディレクトリの指定
DIR = "D:\Coding\点数表"
os.chdir(DIR)
os.getcwd()


# In[5]:


SHOHOSEN_CODE = pdread.read_csv_nohead('処方箋交付.csv')
SHOHOSEN_CODE.columns = ['診療行為コード']
SHOHOSEN_CODE[:5]


# ## GET FOLDER NAMES

# In[6]:


# ディレクトリの指定
DIR = "D:\DokenPo\med"
os.chdir(DIR)
os.getcwd()


# In[7]:


def forda_list(DIR):
    open_name = os.listdir(DIR)
    return open_name


# In[8]:


def files(forda_DIR):
    open_name = os.listdir(forda_DIR)

    file_list = []
    for i in range(len(open_name)):
        s = open_name[i]
        if s.find('csv') > 0: # 見つからない場合は -1 を返す
            file_list.append(s)
        elif s.find('CSV') > 0:
            file_list.append(s)
    
    return file_list


# In[9]:


for j, folder in enumerate(forda_list(DIR)):
    if j == 0: file_name_dic = {}
    try:
        to_float(folder)
        #print(folder)
        DIR_lower = os.path.join(DIR, folder)
        os.chdir(DIR_lower)
        for i, item in enumerate(files(DIR_lower)):
            if i == 0: file_name_dic[int(folder)] = []
            file_name_dic[int(folder)].append(item)
    except:
        print('Error !! CHECK ERROR !!')


# In[10]:


for f in file_name_dic:
    print(f)


# # CREATE CKD FILES

# In[11]:


DOWN_LOAD_DIR = r'D:\DokenPo\PROCEDURE\SHOHOSEN_KOFU'


# In[ ]:


for folder in file_name_dic:
    DIR_lower = os.path.join(DIR, str(folder))
    os.chdir(DIR_lower)
    si_df = pdread.read_csv('prescriptions_data_med.si.csv')
    id_df = pdread.read_csv('prescriptions_data_med.id.csv')
    ir_df = pdread.read_csv('prescriptions_data_med.ir.csv')
    
    si_df = pd.merge(si_df, id_df, on = 'number_1')
    si_df = si_df[['診療行為コード', '日付_1', '日付_2', '日付_3', '日付_4', '日付_5', '日付_6', '日付_7', '日付_8', '日付_9', '日付_10', 
                   '日付_11', '日付_12', '日付_13', '日付_14', '日付_15', '日付_16', '日付_17', '日付_18', '日付_19', '日付_20', '日付_21', 
                   '日付_22', '日付_23', '日付_24', '日付_25', '日付_26', '日付_27', '日付_28', '日付_29', '日付_30', '日付_31', 'number_1', 
                   '生年月日', '男女区分', 'ID']]
    si_df = pd.merge(si_df, ir_df[['請求年月', 'number_1']], on = 'number_1')
    
    shohosen_df = pd.merge(si_df, SHOHOSEN_CODE, left_on = '診療行為コード', right_on = '診療行為コード')
    shohosen_df = shohosen_df.melt(id_vars = [ 'number_1', '生年月日', '男女区分', '診療行為コード', '請求年月', 'ID'],
                  var_name = '日付', value_name = 'DATA')
    shohosen_df['日付'] = shohosen_df['日付'].apply(lambda x: x.replace('日付_', ''))
    shohosen_df.dropna(subset = ['DATA'], inplace = True)
    
    shohosen_df.to_csv(os.path.join(DOWN_LOAD_DIR, 'SHOHOSEN_from_prescription_' + str(folder) + '.csv'), index = False)


# In[ ]:




