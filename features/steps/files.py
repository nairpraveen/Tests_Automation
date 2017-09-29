import pandas as pd
import os, fnmatch
from dir_file import dir_create

class retrieve_files(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None

	def find(pattern, path):
		result = []
		for file in os.listdir(path):
			if fnmatch.fnmatch(file, '*.txt'):
				total_file_name = file
				if total_file_name[-12:-4] == str(pattern):
					result.append(total_file_name)
			elif fnmatch.fnmatch(file, '*.csv'):
				total_file_name = file
				if total_file_name[-12:-4] == str(pattern):
					result.append(total_file_name)
		return result


	def files(self, date, masterfile_loc,resultsfilelocation):
		masterfile = pd.read_json(masterfile_loc)
		control_def_file_loc = masterfile.controlfile.ix[0]
		controlfile = pd.read_json(control_def_file_loc)
		controlfile_folder = controlfile.filename.ix[0]
		control_data_file = "data/"+controlfile_folder+"/"+retrieve_files.find(date, "data/"+controlfile_folder)[0]
		text_files = masterfile.files
		datafiles_names = []
		deffiles_names = []
		for i in range(0, len(text_files)):
			a = text_files.index[i]
			b = str(text_files[a]['filename'])
			b1 = str(retrieve_files.find(date, "data/"+b)[0])
			c = text_files[a]['filedeffile']
			datafiles_names.append("data/"+b+"/"+b1)
			deffiles_names.append(c)
		return  datafiles_names, deffiles_names, control_data_file, control_def_file_loc