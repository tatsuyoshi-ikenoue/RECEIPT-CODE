import numpy as np
import pandas as pd
import zenhan

class generate():
    def __init__(self, ki, ban, birth, gen):
        self.ki    = zenhan.z2h(str(ki), mode=7, ignore=())
        self.ban   = zenhan.z2h(str(ban), mode=7, ignore=())
        self.birth = zenhan.z2h(str(birth), mode=7, ignore=())
        self.gen   = zenhan.z2h(str(gen), mode=7, ignore=())    
    # 記号処理
    def kigo(self):
        if pd.isna(self.ki):
            self.ki = np.nan
        else:
            if len(str(self.ki)) <= 4:
                self.ki = int(self.ki) + 710000
            else:
                self.ki = int(self.ki)
    # 性別処理
    def gender(self):
        self.gen = int(self.gen)
        if self.gen == 1: self.gen = str(1).zfill(6)
        else: self.gen = str(2).zfill(6)
    # ID setting    
    def ID(self):
        def func(item):
            return str(int(item)).zfill(6)
        return func(self.ki) + func(self.ban) + func(self.birth) + func(self.gen)

### Exaple ###
# usage; generate(710001,10006,3510131, 1).ID()
# Output;'7100010100063510131000001'
