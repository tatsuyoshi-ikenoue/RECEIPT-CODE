#!/usr/bin/env python
# coding: utf-8

# # FOLDER CHECK

# coding: utf-8
import pandas as pd
import numpy as np
import csv
import os
import sys

DIR = r"D:\土木健保データ原本写し\20191105\提供データ\診療報酬明細書"
#DIR = r"D:\土木健保データ原本写し\20171020\レセプト"
os.chdir(DIR)
os.getcwd()

# ## GET FOLDER LIST

def folder_list(DIR):
    open_name = os.listdir(DIR)
    return open_name

folders = folder_list(DIR)

# ## Folder NUmber

print(len(folders))

# ## LIST UP FOLDER

folders

# ## GET FOLDER PATH

for i, folder in enumerate(folders):
    os.chdir(DIR)
    os.getcwd()

    if i == 0: folders_DIR = []
    folders_DIR.append(os.path.join(DIR, folder))

# ## GET FILE PATH

def files(folder_DIR):
    open_name = os.listdir(folder_DIR)

    file_list = []
    for i in range(len(open_name)):
        s = open_name[i]
        if (s.find('csv') > 0) | (s.find('CSV') > 0): # 見つからない場合は -1 を返す
            file_list.append(s)
        else:
            pass
    if len(file_list) > 0 : return file_list
    else : return print(str(folder_DIR) + '　にはcsvファイルがありません。もう一階層下を検索します_(꒪ཀ꒪」∠)_')

for i, folder_DIR in enumerate(folders_DIR):
    if i == 0: FILE_PATH_dic = {}; folders_DIR_update = []

    if len(folder_list(folder_DIR)) == 1:
        #print(folder_list(folder_DIR))
        fs_list = files(os.path.join(folder_DIR, folder_list(folder_DIR)[0]))
        
        for j, f in enumerate(fs_list):
            f_path = os.path.join(os.path.join(folder_DIR, folder_list(folder_DIR)[0]), f)
            
            if j == 0: dum = [f_path]
            else: dum.append(f_path)
           
        FILE_PATH_dic[i] = dum
        if len(FILE_PATH_dic[i]) > 0 :
            print(str(os.path.join(folder_DIR, folder_list(folder_DIR)[0])) + "　にcsvファイルがありました(≧▽≦)")
            print("")
            
        folders_DIR_update.append(os.path.join(folder_DIR, folder_list(folder_DIR)[0]))
        
    else:
        for j, f in enumerate(files(folder_DIR)):
            f_path = os.path.join(folder_DIR,  f)
            
            if j == 0: dum = [f_path]
            else: dum.append(f_path)
                
        FILE_PATH_dic[i] = dum
        
        folders_DIR_update.append(folder_DIR)
        
folders_DIR = folders_DIR_update

# # ASSIGN NUMBER & DIVIDE DATA

# ## DISCRIMINATION for FILEs 

def fdic(folder):
    fnames = files(folder)
    ftuples = []
    for fname in fnames:
        fragm = fname.split('.')[0]
        ftuple = (fname, fragm.split('_')[2].lower())
        ftuples.append(ftuple)
    return {k: v for (k, v) in ftuples}

# ## GET FILE NAME & PRESCRIPTION TYPE
# どの種類のデータを見たいかはここで入力してください
# 「MED」：医科
# 「DPC」：DPC
# 「PHA」：調剤

def get_ptype(folder_DIR):
    fdict = fdic(folder_DIR)
    print(fdict)
    
    for item in fdict:
        if 'MED' in item:
            file_name = item
            
    ptype = fdict[file_name]
    
    return file_name, ptype

# ## IMPORT DATA & ASSIGN NUMBER FOR PRESCRIPTION

def assign_rnum(file_name):
    try:
        f = open(file_name, encoding = 'CP932')
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        lines = [line]
        while line:
            line = f.readline()
            lines.append(line)
        
    except:
        f = open(file_name, encoding = 'utf-8')
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        lines = [line]
        while line:
            line = f.readline()
            lines.append(line)

    f.close
    print(file_name + "を読み込みました")

    df =[]
    for line in lines:
        line = line.replace('\n','') # 改行文字を消去
        line = line.split(',') 
        df.append(line)

    df = pd.DataFrame(df)
    df = df.reset_index(drop=False)
    df = df.dropna(subset=[1])

    df[1] = df[1].astype('str').astype('int16')

    df['number_1'] = df['index'] - df[1] + 2 
    print("レセプトに番号を振りました")
    
    return df

# ## DIVIDE PRESCRIPTIONS DATA

def divide_prescriptions(df, type_):
    
    # 平成２８年４月版 
    dpc_list = ['BU', 'CD', 'CO', 'EX', 'GA', 'GR', 'GT', 'HH', 'HO', 'HR', 'IR', 'IY', 'JY', 'KK', 'KO', 'MK', 'MN', 'RC', 'RE', 'SB', 'SI', 'SJ', 'SK', 'SY', 'TI', 'TO', 'TR', 'TS']
    med_list = ['CO', 'EX', 'GR', 'HO', 'HR', 'IR', 'IY', 'JY', 'KO', 'MK', 'MN', 'RC', 'RE', 'SI', 'SJ', 'SY', 'TI', 'TO', 'TR', 'TS']
    pha_list = ['SH', 'CZ', 'IY', 'CO', 'EX', 'HO', 'HR', 'JY', 'KI', 'KO', 'MK', 'MN', 'RC', 'RE', 'TK', 'TO', 'YK']

    prescriptions = {}
    
    if type_.lower() == 'dpc':
        for dpc in dpc_list:
            prescriptions[dpc.lower()] = df[df[3] == dpc.upper()] 
            prescriptions[dpc.lower()] = prescriptions[dpc.lower()].dropna(how='all', axis=1)
        del df

    elif type_.lower() == 'med':
        for med in med_list:
            prescriptions[med.lower()] = df[df[3] == med.upper()]
            prescriptions[med.lower()] = prescriptions[med.lower()].dropna(how='all', axis=1)
        del df

    elif type_.lower() == 'pha':
        for pha in pha_list:
            prescriptions[pha.lower()] = df[df[3] == pha.upper()]
            prescriptions[pha.lower()] = prescriptions[pha.lower()].dropna(how='all', axis=1)
            
        # shcziy fileを作成
        shcziy = df[df[3] == 'SH']
        shcziy = shcziy.append(df[df[3] == 'CZ'])
        shcziy = shcziy.append(df[df[3] == 'IY'])
        # sh fileを作成
        sh = df[df[3] == 'SH'] 
        sh = sh['index']
        sh = sh.reset_index(drop=False)
        sh = sh.rename(columns={'level_0': 'sh_num'})
            
        # 分割のための区切りを作成
        sh_list = []
        for j in range(int(len(shcziy)/1000)):
            dum = 0
            for i in sh['sh_num']:
                if i > dum and i < 1000*(j+1): dum = i
                if i > 1000*(j+1): break
            sh_list.append(dum)
        # ファイルを分割
        shcziy_dic = {}
        sh_dic = {}
        for i in range(len(sh_list)):
            if i == 0:
                shcziy_dic[i] = shcziy[(shcziy['index'] < sh_list[i])]
                sh_dic[i] = sh[(sh['sh_num'] < sh_list[i])]
            else:
                shcziy_dic[i] = shcziy[(shcziy['index'] < sh_list[i]) & (shcziy['index'] >= sh_list[i-1])]
                sh_dic[i] = sh[(sh['sh_num'] < sh_list[i]) & (sh['sh_num'] >= sh_list[i-1])]
            
        for i in range(len(sh_list)):
            shcziy_dic[i] = pdbj.merge(left = shcziy_dic[i], right = sh_dic[i], 
                                        left_on=[pdbj.LE('index')], right_on=['sh_num'], 
                                        how='left', sort = True)
            shcziy_dic[i] = shcziy_dic[i][shcziy_dic[i]['sh_num'] == shcziy_dic[i].groupby(['index_x'])['sh_num'].transform(max)]

            if i == 0:
                shcziy_t = shcziy_dic[i]
            else:
                shcziy_t = shcziy_t.append(shcziy_dic[i])                
                
        shcziy_list = ['SH', 'CZ', 'IY']
        for pha in shcziy_list:
            prescriptions[pha.lower()] = shcziy_t[shcziy_t[3] == pha.upper()]                
            prescriptions[pha.lower()] = prescriptions[pha.lower()].dropna(how='all', axis=1)    
        
    else:
        print('「med」：医科、「dpc」：DPC、「pha」：調剤を入力してください')
        sys.exit()
    
    
    return prescriptions 

# ## WRIGHT DOWN TO CSV

# ### WRIGHT DOWN BODY

def writing(prescriptions, ptype, type_DIR, type_list, cym):
    for rsname_l in type_list:
        #try:
            DIR = r'D:\Python\Jupyter\DokenPo'
            raw_DIR = os.path.join(DIR, ptype)
            os.chdir(raw_DIR)            

            rsname = rsname_l.lower()
            fname = 'raw_data_' + ptype + '.' + rsname  + '.csv'

            csv_file = open(fname, 'r', encoding='utf-8')
            f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)

            raw =[]
            for line in f:
                raw.append(line)
            raw_name = {int(k): v for [k, v] in raw}
            prescriptions[rsname] = prescriptions[rsname].rename(columns = raw_name)
            
            folder_DIR = os.path.join(type_DIR, cym)
            os.chdir(folder_DIR)

            dlname = 'prescriptions_data_' + ptype + '.'+ rsname  +'.csv'
            prescriptions[rsname].to_csv(dlname, index=False)
            
        #except:
        #    continue

# ### NAMING FOR DATA

def naming(prescriptions, ptype):
    # 平成２８年４月版 
    dpc_list = ['BU', 'CD', 'CO', 'EX', 'GA', 'GR', 'GT', 'HH', 'HO', 'IR', 'IY', 'JY', 'KK', 'KO', 'MK', 'MN', 'RC', 'RE', 'SB', 'SI', 'SJ', 'SK', 'SY', 'TI', 'TO', 'TR', 'TS']
    med_list = ['CO', 'EX', 'GR', 'HO', 'HR', 'IR', 'IY', 'JY', 'KO', 'MK', 'MN', 'RC', 'RE', 'SI', 'SJ', 'SY', 'TI', 'TO', 'TR', 'TS']
    pha_list = ['SH', 'CZ', 'IY', 'CO', 'EX', 'HO', 'HR', 'JY', 'KI', 'KO', 'MK', 'MN', 'RC', 'RE', 'TK', 'TO', 'YK']

    if ptype == 'pha':
        prescriptions['yk'].reset_index(drop=True, inplace=True)
        cym = prescriptions['yk'].iloc[0,10]
        
    elif ptype == 'med' or 'dpc':
        prescriptions['ir'].reset_index(drop=True, inplace=True)
        cym = prescriptions['ir'].iloc[0,11]

    DIR = r'D:\DokenPo'
    type_DIR = os.path.join(DIR, ptype)
    os.chdir(type_DIR)
    cym = str(cym)
    try: os.mkdir(cym)
    except: pass
        
    if ptype == 'pha': type_list = pha_list
    elif ptype == 'med': type_list = med_list
    else: type_list = dpc_list
        
    print(type_list)
        
    writing(prescriptions, ptype, type_DIR, type_list, cym)

