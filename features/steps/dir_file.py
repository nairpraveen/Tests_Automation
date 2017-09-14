import pandas as pd
import glob, os, datetime
from datetime import date
import shutil

class dir_create(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None

	def dir(self):
		pass_list = []
		fail_list = []
		today = date.today()
		mydir_pass = os.path.join(os.getcwd(), "Result", "Pass", str(today))
		mydir_fail = os.path.join(os.getcwd(), "Result", "Failed", str(today))
		if not os.path.exists(mydir_pass):
		    os.makedirs(mydir_pass)
		else:
			files = glob.glob(mydir_pass+"*.txt")
			for f in files:
				os.remove(f)

		if not os.path.exists(mydir_fail):
		    os.makedirs(mydir_fail)
		else:
			files = glob.glob(mydir_pass+"*.txt")
			for f in files:
				os.remove(f)

		return (mydir_pass, mydir_fail)
