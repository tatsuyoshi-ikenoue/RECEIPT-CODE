import pandas as pd

class csv():
	def __init__(self, dir):
		self.dir = dir
	def headder(self):
		try: return pd.read_csv(self.dir, encoding = 'cp932', engine = 'python')
		except: return pd.read_csv(self.dir, encoding = 'utf-8', engine = 'python')
	def noheadder(self):
		try: return pd.read_csv(self.dir, encoding = 'cp932', engine = 'python', header = None)
		except: return pd.read_csv(self.dir, encoding = 'utf-8', engine = 'python', header = None)
