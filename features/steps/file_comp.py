import pandas as pd
from pathlib import Path
import json
import os, glob
import filecmp

class f_comp(object):
	"""docstring for Count"""


	def __init__(self):
		self.fn = None


	def comp(self, text_file_summary_result, resultsfilelocation):

		final_result, result = {}, {}
		my_file = Path(text_file_summary_result)
		if my_file.exists():
			file_list = sorted(os.listdir(resultsfilelocation+"Summary_Result"+"/"), key=os.path.getctime)

			if len(file_list) > 1:

				with open(resultsfilelocation+"Summary_Result"+"/"+file_list[len(file_list)-1]+"/"+"summary_result.json", 'r') as datafile:
					latest_data = json.load(datafile)
				latest_data = pd.DataFrame(latest_data)
				#print(latest_data)

				with open(resultsfilelocation+"Summary_Result"+"/"+file_list[len(file_list)-2]+"/"+"summary_result.json", 'r') as datafile:
					previous_latest_data = json.load(datafile)
				previous_latest_data = pd.DataFrame(previous_latest_data)
				#print(previous_latest_data)

				for i in range(0, len(latest_data.ix[1].index)):
					for j in range(0, len(previous_latest_data.ix[1].index)):
						# if latest_data.ix[1].index[i] == previous_latest_data.ix[1].index[j] and latest_data.ix[1][i] == "Pass" and previous_latest_data.ix[1][i] == "Pass":
						# 	print(latest_data.ix[1].index[i],"...................")
						# 	line = filecmp.cmp(resultsfilelocation+file_list[len(file_list)-1]+"/"+"Pass"+"/"+latest_data.ix[1].index[i], resultsfilelocation+file_list[len(file_list)-2]+"/"+"Pass"+"/"+previous_latest_data.ix[1].index[i])
						print(latest_data.ix[1].index[i])
						print(previous_latest_data.ix[1].index[j])
						print(latest_data.ix[1][i])
						print(previous_latest_data.ix[1][i])
						#print(my_file + "hi----------------")
						if latest_data.ix[1].index[i] == previous_latest_data.ix[1].index[j] and latest_data.ix[1][i] == "Failed" and previous_latest_data.ix[1][i] == "Pass":
							line = filecmp.cmp(resultsfilelocation+file_list[len(file_list)-1]+"/"+"Failed"+"/"+latest_data.ix[1].index[i], resultsfilelocation+file_list[len(file_list)-2]+"/"+"Pass"+"/"+previous_latest_data.ix[1].index[i])
							if line == "False":
								line = ["The file is different from the Previous created file"]
							else:
								line = ["The file has no conflicts"]
						else:
							line = ["The File has no conflicts because it's a newly created file"]

						result[latest_data.ix[1].index[i]] = line
					final_result[file_list[len(file_list)-1]] = result
				with open(resultsfilelocation+"SUMMARY_FILE.json", 'a') as f2:
					json.dump(final_result, f2, indent=4)
				f2.close()
