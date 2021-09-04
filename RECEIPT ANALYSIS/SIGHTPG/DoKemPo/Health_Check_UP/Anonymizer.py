#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from pdread import csv
from hashlib import sha256
import numpy as np

df = csv(r"D:\土木健保データ原本写し\特定健診\H30_Specific_Health_Checkups.csv").headder()

def to_str(let):
    try: return let = str(let)
    except: return let = "記載なし"

def anonymize(series):
    return [sha256(to_str(ID).encode('utf-8')).hexdigest() for ID in series]

for item in ['受診者漢字氏名','受診者カナ氏名', "健康診断を実施した医師の氏名"]:
    df[item] = anonymize(df[item])

df.to_csv(r"D:\土木健保データ原本写し\特定健診\H30_Specific_Health_Checkups.csv", index = False)
