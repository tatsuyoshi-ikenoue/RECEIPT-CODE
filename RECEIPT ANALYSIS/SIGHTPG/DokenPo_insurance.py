import numpy as np
import pandas as pd
import datetime
import zenhan

def num(x):
    return str(int(x)).zfill(6)

def char(x):
    return str(int(x)).zfill(6)
    
def gender(x):
    try:
        x = int(x)
        if x == 1: x = 1
        elif x == 5: x = 2
        else: x = 2
    except:
        if x == '男': x = 1
        elif x == '女': x = 2
    return str(int(x)).zfill(6)

def reset_ymd(x):
    if pd.isna(x): return np.nan
    else:
        try:
            birth_ymd = str(int(x))
            y = int(birth_ymd[:4])
            m = birth_ymd[4:6]
            d = birth_ymd[6:]
        except:
            birth_ymd = x
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

def to_gregorian(x):
	g = str(x)[:1]
	y = int(str(x)[1:3])
	m = int(str(x)[3:5])
	d = int(str(x)[5:] )
	if g == '4' : y = y + (1989 - 1)
	elif g == '5' : y = y + (2019 - 1)
	else: return print("Error in this DATE DATA")
	return datetime.date(y, m, d)
            
def kigo(x):
    if pd.isna(x):
        return np.nan
    else:
    	if len(str(x)) <= 4:
            try:
                return int(x)+710000
            except:
                return np.nan
    	else:
    	    return int(x)
            
def timecontroller(x):
    if pd.isna(x):
        return np.nan
    else:
        try:
            x = re.split('\s', str(x))
            return x[0]
        except:
            return np.nan
            

def id_create(kigo, bango, birth_ymd, gender):
    def func(item):
        return str(int(item)).zfill(6)
    return func(kigo) + func(bango) + func(birth_ymd) + func(gender)
    
def med_facility(tdfk, facid):
	tdfk  = zenhan.z2h(tdfk, mode=7, ignore=()).zfill(2)
	facid = zenhan.z2h(facid, mode=7, ignore=()).zfill(7)
	return 'M' + tdfk + facid
	
