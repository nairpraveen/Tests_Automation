import pandas as pd
import glob, os, datetime
from datetime import date
import shutil

class dir_create(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None

	def dir(self):
		mydir_pass = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'), "Pass")
		mydir_fail = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'), "Failed")
		mydir_result = os.path.join(os.getcwd(), datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'), "Result")
		if not os.path.exists(mydir_pass):
		    os.makedirs(mydir_pass)

		if not os.path.exists(mydir_fail):
		    os.makedirs(mydir_fail)
		

		if not os.path.exists(mydir_result):
		    os.makedirs(mydir_result)

		return (mydir_pass, mydir_fail, mydir_result)
