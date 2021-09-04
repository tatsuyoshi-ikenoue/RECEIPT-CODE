import pandas as pd

class csv():
    def __init__(self, DIR):
        self.DIR = DIR
    def headder(self):
        try: return pd.read_csv(self.DIR, encoding = 'cp932', engine = 'python')
        except: return pd.read_csv(self.DIR, encoding = 'utf-8', engine = 'python')
    def noheadder(self):
        try: return pd.read_csv(self.DIR, encoding = 'cp932', engine = 'python', header = None)
        except: return pd.read_csv(self.DIR, encoding = 'utf-8', engine = 'python', header = None)

class tsv():
    def __init__(self, DIR):
        self.DIR = DIR
    def headder(self):
        try: return pd.read_csv(self.DIR, encoding = 'cp932', sep = '\t', engine = 'python')
        except: return pd.read_csv(self.DIR, encoding = 'utf-8', sep = '\t', engine = 'python')
    def noheadder(self):
        try: return pd.read_csv(self.DIR, encoding = 'cp932', sep = '\t', engine = 'python', header = None)
        except: return pd.read_csv(self.DIR, encoding = 'utf-8', sep = '\t', engine = 'python', header = None)
