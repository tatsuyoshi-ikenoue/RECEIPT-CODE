# coding: utf-8

import csv
import re
import pandas as pd
import os
import sys
import numpy as np

def adm(target):
    # Folderの指定
    DIR = "D:\\DokenPo\\med\\" + str(target)
    os.chdir(DIR)


    # SI の読み込み
    si_df = pd.read_csv("prescriptions_data_med.si.csv")
    si_df = si_df[['診療行為コード', '数量データ', '点数', '回数', 'コメントコード①', '文字データ①', 'コメントコード②',
           '文字データ②', 'コメントコード③', '文字データ③', '日付_1', '日付_2', '日付_3', '日付_4', '日付_5',
           '日付_6', '日付_7', '日付_8', '日付_9', '日付_10', '日付_11', '日付_12', '日付_13',
           '日付_14', '日付_15', '日付_16', '日付_17', '日付_18', '日付_19', '日付_20', '日付_21',
           '日付_22', '日付_23', '日付_24', '日付_25', '日付_26', '日付_27', '日付_28', '日付_29',
           '日付_30', '日付_31', 'number_1']]

    # RE の読み込み
    re_df = pd.read_csv("prescriptions_data_med.re.csv")
    re_df = re_df[['レセプト種別', '診療年月', '氏名', '男女区分', '生年月日', '給付割合', '入院年月日', 'number_1' ]]
    
    # HO の読み込み
    ho_df = pd.read_csv("prescriptions_data_med.ho.csv")
    ho_df = ho_df[['ds','tsuban','保険者番号', '被保険者証記号', '被保険者証番号', '診療実日数', '合計点数', 'number_1']]
    ho_df.sort_values(by=["number_1", 'tsuban'], ascending = False)
    ho_df.drop_duplicates(subset = "number_1", inplace = True)


    # SI Codeの読み込み
    DIR = r"D:\Coding\SI_code"
    os.chdir(DIR)
    # 入院コードの読み込み
    ddf = pd.read_csv('SI in admission.txt', encoding= 'utf-8', engine='python', header=None )
    ddf.rename(columns={0:'RECEIPT_CODE', 1:'加算名称'}, inplace=True)
    # 短期手術基本料（包括）コードの読み込み
    short_stay_surgery = pd.read_csv('SI about short stay surgery.txt', encoding= 'utf-8', engine='python', header=None )
    short_stay_surgery.rename(columns={0:'RECEIPT_CODE', 1:'加算名称'}, inplace=True)


    # 入院レセプトの判定
    def in_hospital(x):
        if int(x) % 2 == 1:
            inhos = 1
        else: inhos = 0
        return inhos

    re_df['in_hospital'] = re_df['レセプト種別'].apply(in_hospital)

    # 入院レセプトの限定（Main dataの作成）
    in_hosp_df = re_df[re_df['in_hospital'] == 1]
    in_hosp_df = pd.merge(in_hosp_df, si_df , on = 'number_1')


    # Main dataへの入院SIコードの付与
    in_hosp_df = pd.merge(in_hosp_df, ddf, how = 'inner', left_on = '診療行為コード', right_on = 'RECEIPT_CODE')


    # レセプトごとに１行にまとめる
    grouped = in_hosp_df.groupby('number_1')
    in_hosp_com_df = grouped.max()
    in_hosp_com_df.reset_index(drop = False, inplace = True)


    # Main dataを縦持ちに変換する
    in_hosp_com_df = pd.wide_to_long(in_hosp_com_df, stubnames='日付_', i=['number_1', 'レセプト種別', '診療年月', '氏名', '男女区分', '生年月日', '入院年月日', 'in_hospital', '回数',], j='day')
    in_hosp_com_df = in_hosp_com_df[['日付_']]
    in_hosp_com_df.reset_index(drop = False, inplace = True)
           # '日付_'がNaNは入院外、1は入院中


    # 短期滞在手術入院基本料を考慮する
    short_stay_surgery = pd.merge( si_df, short_stay_surgery, how = 'inner', left_on = '診療行為コード', right_on = 'RECEIPT_CODE')

    grouped = short_stay_surgery.groupby(['number_1','加算名称'])
    short_stay_surgery = grouped.max()

    short_stay_surgery.reset_index(drop = False, inplace = True)
    short_stay_surgery = pd.wide_to_long(short_stay_surgery, stubnames='日付_', i=['number_1','加算名称'], j='day')
    short_stay_surgery.reset_index(drop = False, inplace = True)

    short_stay_surgery = short_stay_surgery[['診療行為コード', '加算名称', 'number_1', 'day', '日付_']]
    short_stay_surgery = short_stay_surgery[short_stay_surgery['日付_']==1]

    short_stay_surgery.reset_index(drop = False, inplace = True)
    for i in range(len(short_stay_surgery)):
        if short_stay_surgery['診療行為コード'][i] == 190076710:
            short_stay_surgery['日付_'][i] = np.nan   # 日帰り手術
        elif (short_stay_surgery['診療行為コード'][i] == 190076810) | (short_stay_surgery['診療行為コード'][i] == 190125310):
            short_stay_surgery['日付_'][i] = 2        # １泊２日の手術
        elif (short_stay_surgery['診療行為コード'][i] == 190130410) | (short_stay_surgery['診療行為コード'][i] == 190130510):
            short_stay_surgery['日付_'][i] = 5        # ４泊５日までの手術

    short_stay_surgery.reset_index(drop = False, inplace = True)

    # 短期滞在手術入院基本料２（１泊２日入院）、短期滞在手術入院基本料３（４泊５日入院）の検出
    for item in short_stay_surgery['日付_']:
        if (item == 2) | (item == 5):
            print(str(target))
            print('Warning!!')


    in_hosp_com_df = pd.merge(in_hosp_com_df, short_stay_surgery, how = 'left', on = ['number_1', 'day'])

    for i in range(len(in_hosp_com_df)):
        if in_hosp_com_df['日付__y'][i] == 2:
            in_hosp_com_df['日付__x'][i] = 2
            in_hosp_com_df['日付__x'][i+1] = 2
        elif in_hosp_com_df['日付__y'][i] == 5:
            in_hosp_com_df['日付__x'][i] = 5
            in_hosp_com_df['日付__x'][i+1] = 5
            in_hosp_com_df['日付__x'][i+2] = 5
            in_hosp_com_df['日付__x'][i+3] = 5
            in_hosp_com_df['日付__x'][i+4] = 5
    
    in_hosp_com_df.rename(columns={'日付__x':'日付_'}, inplace=True)
    in_hosp_com_df = in_hosp_com_df[['number_1', 'レセプト種別', '診療年月', '氏名', '男女区分', '生年月日', '入院年月日', 'in_hospital', '回数', 'day', '日付_']]


    in_hosp_com_df = in_hosp_com_df[in_hosp_com_df['日付_']>0]
    in_hosp_com_df['day_from_ad'] = in_hosp_com_df.groupby('number_1')['day'].rank(ascending=True)


    in_hosp_com_df['group'] = in_hosp_com_df['day'] - in_hosp_com_df['day_from_ad'] 


    grouped = in_hosp_com_df.groupby(['number_1', 'group'])
    in_hosp_com_df_start = grouped.min()
    in_hosp_com_df_end = grouped.max()


    in_hosp_df = in_hosp_com_df_start
    in_hosp_df = in_hosp_df[['レセプト種別', '診療年月', '氏名', '男女区分', '生年月日', '入院年月日', '回数', 'day']] 
    in_hosp_df.rename(columns={'回数':'当月入院日数', 'day':'start_day'}, inplace=True)

    def f(x):
        return str(x).zfill(2)
    in_hosp_df['start_day'] = in_hosp_df['start_day'].apply(f) 

    in_hosp_df['診療年月'] = in_hosp_df['診療年月'].astype(str)
    in_hosp_df['start_day'] = in_hosp_df['診療年月'] + in_hosp_df['start_day']


    in_hosp_com_df_end = in_hosp_com_df_end[['day']]
    in_hosp_com_df_end.rename(columns={'day':'end_day'}, inplace=True)

    in_hosp_df = pd.concat([in_hosp_df, in_hosp_com_df_end], axis = 1)

    def f(x):
        return str(x).zfill(2)
    in_hosp_df['end_day'] = in_hosp_df['end_day'].apply(f) 
    in_hosp_df['end_day'] = in_hosp_df['診療年月'] + in_hosp_df['end_day']

    in_hosp_df['診療年月'] = in_hosp_df['診療年月'].astype(int)


    in_hosp_df.reset_index(drop = False, inplace = True)
    in_hosp_df = pd.merge(in_hosp_df, ho_df, how ='left', on = 'number_1')
    
    return in_hosp_df

for i in range(2):
    target =42811 + i
    in_hosp_df = adm(target)
    
    # Fordaの指定
    DIR = "D:\\DokenPo\\med\\" + str(target)
    os.chdir(DIR)
    
    # Dataの保存
    in_hosp_df.to_csv('in_hospital_data_med.csv', index = False)
