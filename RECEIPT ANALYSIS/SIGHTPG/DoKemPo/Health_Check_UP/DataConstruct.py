#!/usr/bin/env python
# coding: utf-8

# IMPORT MODULES
import pandas as pd
import numpy as np
import csv
import os
import sys
import re

class files():
    def __init__(self, folder_DIR):
        self.folder_DIR = folder_DIR
    def csv(self):
        return [oname for oname in os.listdir(self.folder_DIR) if oname.lower().find('csv') > 0 ]
    def xlsx(self):
        return [oname for oname in os.listdir(self.folder_DIR) if oname.lower().find('xlsx') > 0 ]
        
class date_split():
    def __init__(self, ymd, sep):
        self.ymd  = ymd
        self.sep  = sep
    def sep_year(self):
        return self.ymd.split(self.sep)[0] 
    def sep_date(self):
        y = self.ymd.split(self.sep)[0]
        m = self.ymd.split(self.sep)[1]
        d = self.ymd.split(self.sep)[2]
        try: self.d = d.split(' ')[0] # 時刻の入ったものへの対応（dd hh:mm....）
        except: pass
        return (int(y) * 10000) + (int(m) * 100) + int(d)
        
class wareki():
    def __init__(self, ymd):
        self.ymd = ymd
    def conv(self):
        cal = ['0', '1', '2', '3', '4', '5'] 
        year = str(self.ymd)[0:4]
        if self.ymd < 18680908:
            calc_year   = cal[0] + str(year)
        elif self.ymd < 19120730:
            calc_year   = cal[1] + str(int(year) - 1867)
        elif self.ymd < 19261225:
            calc_year   = cal[2] + str(int(year) - 1911)
        elif self.ymd < 19890108:
            calc_year   = cal[3] + str(int(year) - 1925)
        elif self.ymd < 20190501:
            calc_year   = cal[4] + str(int(year) - 1988)
        else:
            calc_year   = cal[5] + str(int(year) - 1988)
        
        md = self.ymd - (int(year) * 10000)
        return (int(calc_year) * 10000) + md

class number():
    def __init__(self, num):
        self.num = num
    def zero(self):
        return str(self.num).zfill(6)

class get_keys(): 
    def __init__(self, dic, val):
        self.dic = dic
        self.val = val
    def by_value(self):
        return [k for k, v in self.dic.items() if v == self.val]

class col():
    def __init__(self, df, col_dic):
        self.df = df
        self.col_dic = col_dic
    def rename(self):
        col_dust = {item: [c for c in list(self.df.columns) if c.find(item) >= 0] 
                    for item in ['生年月日', '記号','番号']}
        #for item in ['生年月日', '記号','番号']:
        #    col_dust[item]   = [c for c in list(self.df.columns) if c.find(item) >= 0]
        col_dust['健診受診日'] = [c for c in list(self.df.columns) if c.find('日') >= 0 and c.find('健診') >= 0 ]
        
        columns = {}
        for key in col_dust.keys():
            for persnum in col_dust[key] :
                dummy = (persnum, key if persnum in self.col_dic[key] else None)
                if dummy[1] is not None: result = dummy
            columns[result[0]] = result[1]
        return self.df.rename(columns=columns)   

def read(fname):
    try: return pd.read_csv(fname, engine='python', encoding='utf8')
    except: return pd.read_csv(fname, engine='python', encoding='cp932')

def tedy(dfcolumns):
    try: 
        dfcolumns.astype(float)    
    except: 
        dfcolumns = dfcolumns.astype(str)
        sep_type  = re.sub('[0-9０-９]', '', dfcolumns[1])[0]
        dfcolumns = pd.Series(np.vectorize(lambda x: date_split(x, sep_type).sep_date())(dfcolumns.values))
        dfcolumns = dfcolumns.astype(float)
    return pd.Series(np.vectorize(lambda x: wareki(x).conv())(dfcolumns.values))

def lam(DataF):
    for date_data in ['健診受診日', '生年月日']:
        DataF[date_data] = tedy(DataF[date_data])
    DataF['記号'] = 710000 + DataF['記号']
    DataF['番号'] = DataF['番号'].apply(lambda x:number(x).zero())
    DataF = DataF.sort_values(by='健診受診日')
    DataF = DataF.reset_index(drop=True)
    return DataF

def df_save(DataF):
    sname = 'H' + str(DataF['健診受診日'][0])[1:3] + '_Specific_Health_Checkups.csv'
    DataF.to_csv(sname, index = False)
    print(sname)    
    
DIR = r"D:\土木健保データ原本写し\特定健診"
os.chdir(DIR)

fcsv  = files(DIR).csv()
fxlsx = files(DIR).xlsx()

for fs in [fcsv, fxlsx]:
    df = [read(fname) for fname in fs]
    col_dic = {'健診受診日': ['健診実施日', '健診受診日'], '生年月日': ['生年月日', '受診者生年月日'], 
               '記号': ['記号', '被保険者証記号'], '番号': ['番号', '被保険者証番号']}
    df = list(map(lambda d: col(d, col_dic).rename(), df))
    df = list(map(lam, df))
    list(map(df_save, df))
