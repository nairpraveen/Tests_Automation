import pandas as pd
from pathlib import Path
import json
import os, glob
import filecmp

class f_comp(object):
	"""docstring for Count"""


	def __init__(self):
		self.fn = None


	def comp(self, text_file_summary_result, resultsfiles_loc):

		final_result, result = {}, {}
		my_file = Path(text_file_summary_result)
		if my_file.exists():

			file_list = sorted(os.listdir(resultsfiles_loc+"Summary_Result"+"/"))

			if len(file_list) > 1:

				with open(resultsfiles_loc+"Summary_Result"+"/"+file_list[len(file_list)-1]+"/"+"summary_result.json", 'r') as datafile:
					latest_data = json.load(datafile)
				latest_data = pd.DataFrame(latest_data)

				with open(resultsfiles_loc+"Summary_Result"+"/"+file_list[len(file_list)-2]+"/"+"summary_result.json", 'r') as datafile:
					previous_latest_data = json.load(datafile)
				previous_latest_data = pd.DataFrame(previous_latest_data)

				for i in range(0, len(latest_data.ix[1].index)):

					if latest_data.ix[1].index[i] == previous_latest_data.ix[1].index[i] and latest_data.ix[1][i] == "Pass" and previous_latest_data.ix[1][i] == "Pass":

						line = filecmp.cmp(resultsfiles_loc+file_list[len(file_list)-1]+"/"+"Pass"+"/"+latest_data.ix[1].index[i], resultsfiles_loc+file_list[len(file_list)-2]+"/"+"Pass"+"/"+previous_latest_data.ix[1].index[i])
						if line == "False":
							result_line = ["The file is different from the Previous created file"]
						else:
							result_line = ["The file has no conflicts"]


					elif latest_data.ix[1].index[i] == previous_latest_data.ix[1].index[i] and latest_data.ix[1][i] == "Failed" and previous_latest_data.ix[1][i] == "Pass":

						line = filecmp.cmp(resultsfiles_loc+file_list[len(file_list)-1]+"/"+"Failed"+"/"+latest_data.ix[1].index[i], resultsfiles_loc+file_list[len(file_list)-2]+"/"+"Pass"+"/"+previous_latest_data.ix[1].index[i])

						if line == "False":
							result_line = ["The file is different from the Previous created file"]
						else:
							result_line = ["The file has no conflicts"]
					else:
						result_line = ["The File has no conflicts because it's a newly created file"]

					result[latest_data.ix[1].index[i]] = result_line
				final_result[file_list[len(file_list)-1]] = result

				with open(resultsfiles_loc+"SUMMARY_FILE.json", 'a') as f2:
					json.dump(final_result, f2, indent=4)
				f2.close()
