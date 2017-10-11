import pandas as pd
import os, fnmatch
from dir_file import dir_create
import re

class retrieve_files(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None

	def find(pattern1, pattern2, pattern3, path):
		result = []
		for file in os.listdir(path):
			if re.search(str(pattern2), file):
				if re.search(str(pattern3), file):
					if fnmatch.fnmatch(file, '*.txt'):
						if re.search(str(pattern1), file):
							result.append(path+file)
					elif fnmatch.fnmatch(file, '*.csv'):
						if re.search(str(pattern1), file):
							result.append(path+file)
		return result


	def files(self, date, masterfile_loc,resultsfilelocation, timestamp):
		try:
			masterfile = pd.read_json(masterfile_loc)
			control_def_file_loc = masterfile.controlfile.ix[0]
			data_file_loc = masterfile.datafilelocation.ix[0]
			# control_data_file = data_file_loc+"/"+"kab_control_"+date+".txt"
			text_files = masterfile.files
			datafiles_names = []
			deffiles_names = []

			for i in range(0, len(text_files)):
				a = text_files.index[i]
				b = str(text_files[a]['filename'])
				datafiles_names.append(retrieve_files.find(date, b, timestamp, data_file_loc+"/"))

				for file in os.listdir(data_file_loc+"/"):
					if re.search(str(b), file):
						if re.search(str(timestamp), file):
							if fnmatch.fnmatch(file, '*.txt'):
								if re.search(str(date), file):
									c = text_files[a]['filedeffile']
									deffiles_names.append(c)
							elif fnmatch.fnmatch(file, '*.csv'):
								if re.search(str(date), file):
									c = text_files[a]['filedeffile']
									deffiles_names.append(c)

			datafiles_names  = set([val for sublist in datafiles_names for val in sublist])
			datafiles_names = sorted(datafiles_names)
			deffiles_names = sorted(set(deffiles_names))
			return datafiles_names, deffiles_names, control_def_file_loc
		except:
			print("MasterJSON File Not Found in the specified path")

