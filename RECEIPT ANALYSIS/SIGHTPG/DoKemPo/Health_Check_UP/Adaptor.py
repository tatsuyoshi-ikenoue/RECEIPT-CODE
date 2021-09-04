#!/usr/bin/env python
# coding: utf-8

# IMPORT DATA
import pandas as pd
import numpy  as np
from   numpy import vectorize
import os
import sys
import re

import zenhan
from   insurance import *
from   eGFR      import *
from   cleans    import * 
from   pdread    import csv

# CURRENT DIR
Cur_DIR = os.getcwd()

# ディレクトリの指定
DIR = "D:\土木健保データ原本写し\特定健診"
os.chdir(DIR)

def files(forda_DIR):
    open_name = os.listdir(forda_DIR)
    file_list = [i for i in open_name if i.lower().find('csv') > 0]
    return file_list

## GET FILES
# ファイル名（Key）の入力形式は['H＊＊_Specific_Health_Checkups']もしくは['R＊＊_Specific_Health_Checkups']の形とすること
for f_name in files(DIR):
    Health_DIC = {f_name: csv(f_name).headder()}

## 年度の付与
for k in Health_DIC:
    h_year = k.split('_')[0]
    if h_year.find('h') > 0:
        Health_DIC[k]['YEAR'] = 1988 + int(h_year.replace('H', ''))
    elif h_year.find('r') > 0:
        Health_DIC[k]['YEAR'] = 2018 + int(h_year.replace('R', ''))

## Hb A1cの統一
for k in Health_DIC:
    if '23' in k:
        jds = np.vectorize(lambda x: cleaning(x).to_float())(Health_DIC[k]['ＨｂＡ１ｃ（ＪＤＳ）'].values)
        Health_DIC[k]['ＨｂＡ１ｃ（ＮＧＳＰ）'] = (np.vectorize(lambda x: hba1c(x).conv_jds())(jds)).tolist()
        del Health_DIC[k]['ＨｂＡ１ｃ（ＪＤＳ）'] 
    elif '24' in k:
        jds = np.vectorize(lambda x: cleaning(x).to_float())(Health_DIC[k]['ＨｂＡ１ｃ（ＪＤＳ）'].values)
        Health_DIC[k]['dum'] = (np.vectorize(lambda x: hba1c(x).conv_jds())(jds)).tolist()
        Health_DIC[k]['ＨｂＡ１ｃ（ＮＧＳＰ）'] = Health_DIC[k]['ＨｂＡ１ｃ（ＮＧＳＰ）'].fillna(Health_DIC[k]['dum'] )
        del Health_DIC[k]['dum']
        del Health_DIC[k]['ＨｂＡ１ｃ（ＪＤＳ）']
        
    try:
        Health_DIC[k] = Health_DIC[k].rename(columns={'ＨｂＡ１ｃ': 'ＨｂＡ１ｃ（ＮＧＳＰ）'})
    except:
        pass
    
    Health_DIC[k]['ＨｂＡ１ｃ（ＮＧＳＰ）'] = [cleans(val).hba1c() for val in Health_DIC[k]['ＨｂＡ１ｃ（ＮＧＳＰ）']]

## 列名の統一
### 列名辞書の作成
# ディレクトリの指定
os.chdir(Cur_DIR)  # Cur_DIR：このコードの存在するDIR
col_name = csv(r'COLUMNS_NAME.csv').headder()
col_name = col_name.set_index("'F_YEAR'")

col_name_dic = {i.replace("'", ""): col_name[i].apply(lambda x: str(x).replace("'", "")) for i in list(col_name.columns)}
for k in Health_DIC:
    y = int(k.split('_')[0].replace('H', ''))
    for col in list(col_name.columns[1:]): 
        Health_DIC[k] = Health_DIC[k].rename(columns=
                                             {str(col_name_dic[col.replace("'", "")][y]).replace("'", ""): col.replace("'", "") })

## INSURANCE の適応
### 性別
for f_name in Health_DIC:
    Health_DIC[f_name]['性別'] = [int(gender(x).conv()) for x in Health_DIC[f_name]['性別']]

### 生年月日
for f_name in Health_DIC:
    Health_DIC[f_name]['生年月日']   = [ymd(dt).to_wa() for dt in Health_DIC[f_name]['生年月日']]
    Health_DIC[f_name]['健診受診日'] = [ymd(dt).to_wa() for dt in Health_DIC[f_name]['健診受診日']]

### 記号
for f_name in Health_DIC:
    Health_DIC[f_name]['記号']   = [kigo(x).kigo() for x in Health_DIC[f_name]['記号']]

## 受検者IDデータの作成
for k in Health_DIC:
    Health_DIC[k] = Health_DIC[k].dropna(subset=['性別',  '生年月日', '番号', '記号'])
    Health_DIC[k]['ID'] = [ident(ki, ban, birth, gen).create() for (ki, ban, birth, gen) in zip(Health_DIC[k]['記号'], Health_DIC[k]['番号'], Health_DIC[k]['生年月日'], Health_DIC[k]['性別'])]

## sCr の修正
for k in Health_DIC:
    Health_DIC[k]['血清クレアチニン'] = [cleans(val).cr() for val in Health_DIC[k]['血清クレアチニン']]

## 血圧の修正
bp_list_ori = [['収縮期血圧（１回目）', '拡張期血圧（１回目）'],
               ['収縮期血圧（２回目）', '拡張期血圧（２回目）'], 
               ['収縮期血圧（その他）', '拡張期血圧（その他）']]
bp_list_mod = [['Sys_BP_1st', 'Dia_BP_1st'],
               ['Sys_BP_2nd', 'Dia_BP_2nd'],
               ['Sys_BP_other', 'Dia_BP_other']]

vec_mod_BP = vectorize(lambda Sys_BP_ori, Dia_BP_ori:  cleanBP(Sys_BP_ori, Dia_BP_ori).mod())

for k in Health_DIC:
    for items_ori, items_mod in zip(bp_list_ori, bp_list_mod):
        try:
            Sys_BP_ori = Health_DIC[k][items_ori[0]].values
            Dia_BP_ori = Health_DIC[k][items_ori[1]].values
        
            modified_BP = vec_mod_BP(Sys_BP_ori, Dia_BP_ori)
            Health_DIC[k][items_mod[0]] = modified_BP[0]
            Health_DIC[k][items_mod[1]] = modified_BP[1]
            
            del Health_DIC[k][items_ori[0]]
            del Health_DIC[k][items_ori[1]]
            
        except:
            pass

## 尿所見の数値化
for k in Health_DIC:
    for items in ['尿糖', '尿蛋白']:
        Health_DIC[k][items] = [qualitative(str(val)).conv() for val in  Health_DIC[k][items] ]

# eGFR の追加
for k in Health_DIC:
    Health_DIC[k]['eGFR_JSN'] = [eGFR(birth, check, gen, cr).jsn() for (birth, check, gen, cr) 
                                 in zip(Health_DIC[f_name]['生年月日'], Health_DIC[f_name]['健診受診日'], 
                                        Health_DIC[k]['性別'], Health_DIC[k]['血清クレアチニン'])]
    Health_DIC[k]['eGFR_EPI_Horio'] = [eGFR(birth, check, gen, cr).jsn() for (birth, check, gen, cr) 
                                       in zip(Health_DIC[f_name]['生年月日'], Health_DIC[f_name]['健診受診日'], 
                                              Health_DIC[k]['性別'], Health_DIC[k]['血清クレアチニン'])]

# WRIGHT DOWN DATA TO CSV
for k in Health_DIC:
    f_name = k.split('_')[0] + '_ADAPTED_' + k.split('_')[2] + '_' + k.split('_')[3] + '.csv' 
    Health_DIC[k].to_csv(f_name, index = False)
