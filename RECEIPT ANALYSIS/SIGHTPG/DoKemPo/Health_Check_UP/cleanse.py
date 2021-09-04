import zenhan
import numpy as np

# DATA CLEANING
class cleaning():
    def __init__(self, dt):
        self.dt = dt
    ## 不要文字の修正
    def to_float(self):
        try: return float(self.dt)
        except:
            try: return float(str(self.dt).lower().replace('l', '').replace('h', ''))
            except: np.nan
    def to_int(self):
        try: return int(self.dt)
        except:
            try: return int(str(self.dt).lower().replace('l', '').replace('h', ''))
            except: np.nan
        
## Hb A1cの統一
class hba1c(cleaning):
    def __init__(self, dt):
        self.dt = dt
    def conv_jds(self):
        self.dt = cleaning(self.dt).to_float()    
        return 1.02 * self.dt + 0.25
        
class cleans(cleaning):
    def __init__(self, dt):
        self.dt = dt
    ## sCr の修正
    def cr(self):
        self.dt = cleaning(self.dt).to_float()
        try:
            if self.dt > 20: return np.nan
            else: return self.dt
        except: pass
    ## HbA1c(NSGP) の修正
    def hba1c(self):
        self.dt = cleaning(self.dt).to_float()
        try:
            if self.dt > 30: return np.nan
            elif self.dt == 0: return np.nan
            else: return self.dt
        except: pass

## 尿所見の数値化
class qualitative():
    def __init__(self, qual):
        self.qual = str(qual)
    def conv(self):
        q_dic = {dt: i + 1 for i, dt in enumerate(['－', '±', '１＋', '２＋', '３＋'])}
        self.qual = zenhan.h2z(self.qual, mode=7, ignore=())
        try: return q_dic[self.qual]
        except: pass

## 血圧の修正
class cleanBP(cleaning):
    def __init__(self, Sys_BP_ori, Dia_BP_ori):
        self.Sys_BP_ori = Sys_BP_ori
        self.Dia_BP_ori = Dia_BP_ori
    def mod(self):
        try:
            self.Sys_BP_ori = cleaning(self.Sys_BP_ori).to_float()
            self.Dia_BP_ori = cleaning(self.Dia_BP_ori).to_float()
            if self.Dia_BP_ori > self.Sys_BP_ori: 
                self.Sys_BP_mod = self.Dia_BP_ori
                self.Dia_BP_mod = self.Sys_BP_ori
            else:
                self.Sys_BP_mod = self.Sys_BP_ori
                self.Dia_BP_mod = self.Dia_BP_ori
            if (self.Sys_BP_mod > 300) | (self.Sys_BP_mod == 0): self.Sys_BP_mod = np.nan
            if (self.Dia_BP_mod > 300) | (self.Dia_BP_mod == 0): self.Dia_BP_mod = np.nan   
        except:
            self.Sys_BP_mod = np.nan
            self.Dia_BP_mod = np.nan
        return self.Sys_BP_mod, self.Dia_BP_mod

if __name__ == '__main__':
    cleaning('197.58l').to_float()
    cleans('7.58l').cr()
    qualitative('2+').conv()
    hba1c('7.9h').conv_jds()
    cleanBP('200H', '60').mod()
