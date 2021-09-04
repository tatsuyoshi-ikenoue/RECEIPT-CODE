#!/usr/bin/env python
# coding: utf-8

from insurance import *
import pandas as pd
import numpy as np
import math

class age(ymd):
    def __init__(self, birth, check):
        self.birth = birth
        self.check = check
    def calc(self):
        self.birth = ymd(int(ymd(self.birth).to_wa())).to_gregorian()
        self.check = ymd(int(ymd(self.check).to_wa())).to_gregorian()
        return int((self.check - self.birth).days) / 365.25 

class eGFR(age, gender):
    def __init__(self, birth, check, gen, cr):
        self.birth = birth
        self.check = check
        self.gen   = gen  
        self.cr    = cr
        
    def jsn(self):
        ''''
         日本腎臓学会の式
         https://www.jsn.or.jp/ckd/pdf/CKD01.pdf
         eGFR（mL／分／1.73 m2）＝194×Cr－1.094×Age－0.287（ 女性はこれに×0.739）
        '''' 
        self.age = age(self.birth, self.check).calc()
        self.gen = gender(self.gen).conv()
        m_egfr = 194 * pow(self.cr, (-1.094)) * pow(self.age, (-0.287))
        if self.gen == 2: return 0.739 * m_egfr
        else: return m_egfr      
        
    def epi(self):
        ''''
         日本腎臓学会の式
         https://www.jsn.or.jp/ckd/pdf/CKD01.pdf
         $ eGFR = 0.813\times 141\times min(SCr/\kappa,1)^{\alpha} \times max(SCr/\kappa,1)^{-1.209}\times 0.993^{Age}\times 1.018 [if female]\times 1.159 [if black] $ 
         $ SCr is serum creatinine $<br>
         $ \kappa : 0.7  females, 0.9  males $<br>
         $ \alpha : -0.329  females, -0.411  males $
        '''' 
        self.age = age(self.birth, self.check).calc()
        self.gen = gender(self.gen).conv()
        if self.gen == 2: 
            lim_cr = 0.7
            a   = -0.329
            if self.cr < lim_cr:
                return (0.813 * 141 * pow(self.cr/lim_cr, a) * pow(0.993, self.age)) * 1.018
            else:
                return (0.813 * 141 * pow(self.cr/lim_cr, (-1.209)) * pow(0.993, self.age)) * 1.018
        else: 
            lim_cr = 0.9
            a   = -0.411         
            if self.cr < lim_cr:
                return (0.813 * 141 * pow(self.cr/lim_cr, a) * pow(0.993, self.age))
            else:
                return (0.813 * 141 * pow(self.cr/lim_cr, (-1.209)) * pow(0.993, self.age))    
