import pandas as pd

def read_csv(dir):
	try: return pd.read_csv(dir, encoding = 'cp932', engine = 'python')
	except: return pd.read_csv(dir, encoding = 'utf-8', engine = 'python')
	
def read_csv_nohead(dir):
	try: return pd.read_csv(dir, encoding = 'cp932', engine = 'python', header = None)
	except: return pd.read_csv(dir, encoding = 'utf-8', engine = 'python', header = None)