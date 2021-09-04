import pandas as pd
import numpy  as np
from generateID import *
from pdread import *
import os

class CREATE(generate):
    def __init__(fname_re, fname_ho):
        self.fname_re = fname_re
        self.fname_ho = fname_ho
    def identify(self):
        re_df = csv(fname_re).headder()
        re_df.sort_values(["number_1", "ds"], ascending = False, inplace = True)
        re_df.drop_duplicates(subset = 'number_1', inplace = True)
        try:
            re_df = re_df[['レセプト番号', 'レセプト種別', '診療年月', '氏名', '男女区分', 
                           '生年月日', 'number_1']]
        except:
            re_df = re_df[['レセプト番号', 'レセプト種別', '調剤年月', '氏名', '男女区分', 
                           '生年月日', 'number_1']]
        
        ho_df = csv(fname_ho).headder()
        ho_df.sort_values(["number_1", "ds"], ascending = False, inplace = True)
        ho_df.drop_duplicates(subset = 'number_1', inplace = True)
        ho_df = ho_df[['保険者番号', '被保険者証記号', '被保険者証番号', 'number_1']]
        
        id_df = pd.merge(re_df, ho_df, on = 'number_1')
        id_df['ID'] = [generate(ki, ban, birth, gen).ID() for ki, ban, birth, gen 
                       in zip(id_df['被保険者証記号'], id_df['被保険者証番号'], id_df['生年月日'], id_df['男女区分'])]
        return id_df[['ID', 'number_1']]
    
if __name__ == '__main__':
    TARGET  = ("med","med_id") 
    PATH    = os.path.join(r".\sample", TARGET[0])
    PATH_id = os.path.join(r".\sample", TARGET[1])
    file_list = os.listdir(PATH)
    for f in file_list:
        try:
            os.chdir(os.path.join(PATH, f))
            fname_re = "prescriptions_data_" + TARGET[0] + ".re.csv"
            fname_ho = "prescriptions_data_" + TARGET[0] + ".ho.csv"
            id_df = CREATE(fname_re, fname_ho).identify()
            id_df.to_csv(os.path.join(PATH_id, "prescriptions_data_" + TARGET[0] + f + ".id.csv"), index = False)
        except:
            pass
