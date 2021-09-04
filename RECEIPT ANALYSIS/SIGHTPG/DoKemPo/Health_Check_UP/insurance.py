import numpy as np
import pandas as pd
import datetime
import zenhan

class zero():
    def __init__(self, x):
        self.x = x
    def num(self):
        return str(int(self.x)).zfill(6)
    
class gender(zero):
    def __init__(self, sex):
        self.sex = sex
    def conv(self):
        try:
            self.sex = int(self.sex)
            if self.sex == 1: self.sex = 1
            elif self.sex == 5: self.sex = 2
            else: self.sex = 2
        except:
            if self.sex == '男': self.sex = 1
            elif self.sex == '女': self.sex = 2
        return zero(self.sex).num()

class ymd():
    def __init__(self, x):
        self.x = x
    def to_wa(self):
        if pd.isna(self.x): return np.nan
        else:
            try:
                birth_ymd = str(int(self.x))
                y = int(birth_ymd[:4])
                m = birth_ymd[4:6]
                d = birth_ymd[6:]
            except:
                birth_ymd = self.x
                y = int(birth_ymd.split('/')[0])
                m = birth_ymd.split('/')[1].zfill(2)
                d = birth_ymd.split('/')[2].zfill(2)
            
            if len(str(y) + str(m) + str(d)) > 7:
                md = m + d
                if y < 1912:
                    y = '1' + str(y - 1868 + 1).zfill(2) # 明治
                elif y == 1912:
                    if md < '0730':
                        y = '1' + str(y - 1868 + 1).zfill(2) # 明治
                    else:
                        y = '2' + str(y - 1912 + 1).zfill(2) # 大正
                elif y < 1926:
                    y = '2' + str(y - 1912 + 1).zfill(2) # 大正    
                elif y == 1926:
                    if md < '1226':
                        y = '2' + str(y - 1912 + 1).zfill(2) # 大正
                    else:
                        y = '3' + str(y - 1926 + 1).zfill(2) # 昭和
                elif y < 1989:
                    y = '3' + str(y - 1926 + 1).zfill(2) # 昭和
                elif y == 1989:
                    if md < '0108':
                        y = '3' + str(y - 1926 + 1).zfill(2) # 昭和
                    else:
                        y = '4' + str(y - 1989 + 1).zfill(2) # 平成
                elif y < 2019:
                    y = '4' + str(y - 1989 + 1).zfill(2) # 平成
                elif y == 2019:
                    if md < '0501':
                        y = '4' + str(y - 1989 + 1).zfill(2) # 平成
                    else:
                        y = '5' + str(y - 2019 + 1).zfill(2) # 令和
                else:
                    y = '5' + str(y - 2019 + 1).zfill(2) # 令和
                return y + m + d
            else: return str(y) + str(m) + str(d)
    
    def to_gregorian(self):
        g = str(self.x)[:1]
        y = int(str(self.x)[1:3])
        m = int(str(self.x)[3:5])
        d = int(str(self.x)[5:] )
        if   g == '1' : y = y + (1868 - 1)
        elif g == '2' : y = y + (1912 - 1)
        elif g == '3' : y = y + (1926 - 1)
        elif g == '4' : y = y + (1989 - 1)
        elif g == '5' : y = y + (2019 - 1)
        else: return print("Error in this DATE DATA")
        return datetime.date(y, m, d)
    
    def timecontroller(self):
        if pd.isna(self.x): return np.nan
        else: 
            try: return re.split('\s', str(self.x))[0]
            except: return np.nan		

	
class kigo():
    def __init__(self, x):
        self.x = x
    def kigo(self):
        if pd.isna(self.x): return np.nan
        elif len(str(self.x)) <= 4:
            try: return int(self.x)+710000
            except: return np.nan
        else: return int(self.x)


class ident(zero, kigo):
    def __init__(self, ki, ban, birth, gen):
        self.ki = ki
        self.ban = ban
        self.birth = birth
        self.gen = gen
    def create(self):
        self.ki = kigo(self.ki).kigo()
        return zero(self.ki).num() + zero(self.ban).num() + zero(self.birth).num() + zero(self.gen).num()
    

class facility():
    def __init__(self, tdfk, facid):
        self.tdfk  = tdfk
        self.facid = facid
    def med(self):
        self.tdfk  = zenhan.z2h(self.tdfk, mode=7, ignore=()).zfill(2)
        self.facid = zenhan.z2h(self.facid, mode=7, ignore=()).zfill(7)
        return 'M' + self.tdfk + self.facid
