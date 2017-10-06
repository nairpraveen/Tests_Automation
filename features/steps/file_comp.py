import pandas as pd
from pathlib import Path
import json
import os, glob, re
import filecmp

class f_comp(object):
	"""docstring for Count"""


	def __init__(self):
		self.fn = None


	def comp(self, text_file_summary_result, datafiles_names, timestamp, resultsfiles_loc):

		final_result, result = {}, {}
		my_file = Path(text_file_summary_result)
		pass_file_list = os.listdir(resultsfiles_loc+"Pass"+"/")
		fail_file_list = os.listdir(resultsfiles_loc+"Failed"+"/")
		result_line = []

		if len(pass_file_list):

			for file in pass_file_list:
				for file1 in fail_file_list:
					for i in range(0, len(datafiles_names)):
						client_file = datafiles_names[i]
						client_file_name = client_file.split('/')[1]

						if re.search(str(timestamp), client_file_name):
							file_name_without_ts = client_file_name.rsplit(timestamp, 1)[0]

							if re.search(str(file_name_without_ts), str(file)):
								line = filecmp.cmp(resultsfiles_loc+"Pass"+"/"+file, resultsfiles_loc+"Pass"+"/"+file)
								if line == "False":
									result_line = ["The file is different from the Previous created file"]
								else:
									result_line = ["The file has no conflicts"]

							elif re.search(str(file_name_without_ts), str(file1)):
								if re.search(str(file_name_without_ts), str(file)):
									line = filecmp.cmp(resultsfiles_loc+"Failed"+"/"+client_file_name, resultsfiles_loc+"Pass"+"/"+file)
									if line == "False":
										result_line = ["The file is different from the Previous created file"]
									else:
										result_line = ["The file has no conflicts"]
							else:
								result_line = ["The File has no conflicts because it's a newly created file"]
						result[client_file_name] = result_line
		else:
			result_line = ["There are no passed files to compare"]
		
		print(result,"--------------------------")

		with open(resultsfiles_loc+"SUMMARY_FILE.json", 'a') as f2:
			json.dump(result, f2, indent=4)
		f2.close()
