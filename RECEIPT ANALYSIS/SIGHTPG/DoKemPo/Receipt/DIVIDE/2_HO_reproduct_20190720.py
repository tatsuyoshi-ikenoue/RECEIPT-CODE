#!/usr/bin/env python
# coding: utf-8

# # IMPUT TARGET TYPE

Target = 'pha'

# # IMPORT DATA

import csv
import re
import pandas as pd
import os
import sys
import numpy as np
import zenhan
from pdread import *
import datetime

def inskigo(x):
    x = zenhan.z2h(text=str(x), mode=7, ignore=())
    x = re.sub('\s', '', x)
    x = re.sub('\D', '', x)
    if len(x) == 6:
        return x
    elif len(x) == 4:
        return str(710000 + int(x))
    else: return x

# ## GET FILE DiRECTORY

DIR = os.path.join("D:\DokenPo", str(Target))
os.chdir(DIR)

open_name = os.listdir(DIR)
forda_name = pd.DataFrame(open_name)
forda_name['DIR_Name'] = forda_name[0].apply(lambda x: os.path.join(DIR, x))

if str(Target).lower == 'pha':
    read_list = ['HO', 'CZ', 'RE', 'IY']
else:
    read_list = ['HO', 'RE', 'IY']

for item in read_list:
    name_dir = item.upper() + '_name'
    file_name = 'prescriptions_data_' + str(Target) + '.' + item.lower() + '.csv'
    forda_name[name_dir] = forda_name['DIR_Name'].apply(lambda x: os.path.join(x, file_name))

# ## IMPORT PERFORMED DATA

try:
    performed_path = os.path.join("D:\Python\Jupyter\DokenPo", str(Target), "performed_data.csv")
    performed_df   = csv(performed_path).headder()
except:
    cols = ['file', 'date']
    performed_df = pd.DataFrame(index=[], columns=cols) 
    performed_df.to_csv(performed_path, index = False)

# ## DELETE CHANGED HO-information

if len(performed_df) > 0:
    for item in performed_df['file']:
        forda_name = forda_name[forda_name[0] != str(item)]

# # PROCEDURE FOR HO

df_HO = {}
for item, f_info in zip(forda_name['HO_name'], forda_name[0]):
    try:
        df_HO = csv(item).headder()
        df_HO.sort_values(by=['number_1', 'ds'], ascending=False, inplace = True)
        df_HO.drop_duplicates(subset = ['number_1'], inplace = True)
        df_HO['被保険者証記号'] = df_HO['被保険者証記号'].apply(inskigo)
        
        df_HO['被保険者証番号'] = df_HO['被保険者証番号'].apply(lambda x:zenhan.z2h(text=str(x), mode=7, ignore=()))

        df_HO = df_HO.to_csv(item, index = False)
        
        ## PERFORMED DATAに処理記録を保存
        temp_df = pd.DataFrame([f_info, datetime.date.today()]).T

        temp_df.columns = ['file', 'date']
        performed_df = performed_df.append(temp_df)
    
    except:
        print(item + ' では何もしませんでした')

# # WRIGHT DOWN PERFORMED DATA

performed_df
performed_df.to_csv(performed_path, index = False)


