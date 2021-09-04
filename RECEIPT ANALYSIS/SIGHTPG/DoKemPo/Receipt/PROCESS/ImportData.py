import pandas as pd
import pdread 
import numpy as np
import os
from toolz.dicttoolz import valmap
from generateID import generate

## get folder list
DIR = r'.\sample'
os.chdir(DIR)
flist = os.listdir()

## target term
def terget_term(ym):
    t_list = [fname for fname in flist if fname > '4' + str(ym)]
    del t_list[-1]
    return t_list

## import data
ho = {tname: pdread.read_csv(os.path.join(tname, 'prescriptions_data_med.ho.csv')) for tname in terget_term(2806)}
ir = {tname: pdread.read_csv(os.path.join(tname, 'prescriptions_data_med.ir.csv')) for tname in terget_term(2806)}
re = {tname: pdread.read_csv(os.path.join(tname, 'prescriptions_data_med.re.csv')) for tname in terget_term(2806)}

## set up form
def ho_form(x):
    x.sort_values(['tsuban', 'ds'], ascending = False, inplace = True)
    x.drop_duplicates(subset = 'number_1', inplace = True)
    return x[['保険者番号', '被保険者証記号', '被保険者証番号', '診療実日数', '合計点数', 
              '食事療養_生活療養回数', '食事療養_生活療養合計金額', '職務上の理由', '証明書番号', 
              '負担金額医療保険', '負担金額減免区分', '負担金額減額割合', '負担金額減額金額', 'number_1']]
def ir_form(x):
    x.sort_values(['tsuban', 'ds'], ascending = False, inplace = True)
    x.drop_duplicates(subset = 'number_1', inplace = True)
    return x[['都道府県', '点数表', '医療機関コード', '医療機関名称', '請求年月', '電話番号', 'number_1']]
def re_form(x):
    x.sort_values(['tsuban', 'ds'], ascending = False, inplace = True)
    x.drop_duplicates(subset = 'number_1', inplace = True)
    return x[['診療年月', '氏名', '男女区分', '生年月日', '給付割合', '入院年月日', '病棟区分', 'number_1']]

## apply form
ho = valmap(ho_form, ho)
ir = valmap(ir_form, ir)
re = valmap(re_form, re)


def mert(k):
    df = pd.merge(re[k], ho[k], on = 'number_1')
    return pd.merge(df, ir[k], on = 'number_1')
keys = [k for k, v in ho.items()]
df   = {k: mert(k) for k in keys}


def gen(df):
    a = {k: df[item].to_numpy() for k, item in zip(["ki_array", "ban_array", "birth_array", "gen_array"], 
                      ['被保険者証記号', '保険者番号', '生年月日','男女区分'])}
    def g(ki, ban, birth, gen):
        return generate(ki, ban, birth, gen).ID()
    df['ID'] = np.vectorize(g)(a["ki_array"], a["ban_array"], a["birth_array"], a["gen_array"]).tolist()
    return df


d = valmap(gen, df)
