import pandas as pd
import glob, os, datetime
from dir_file import dir_create
from datetime import date
# from file_comp import file_comp
import json

class scenario(object):
	"""docstring for Count"""

	def __init__(self):
		self.fn = None


	def control_file_values(control_file, sep_value):

		temp = pd.read_csv(control_file, sep='|')
		df = pd.DataFrame()
		df['NumberOfRows'] = temp['FileName'].apply(lambda x: x.split(sep_value)[1])
		df['FileName'] = temp['FileName'].apply(lambda x: x.split(sep_value)[0])
		df = df.groupby('FileName').sum()
		return df


	def seperator_value(def_file_name):
		sep_value = pd.read_json(def_file_name)
		sep_value = sep_value.fieldseparator.ix[0]
		return sep_value


	def scenario_writing_to_files(self, today_now, resultsfilelocation, datafiles_names, deffiles_names, control_file, control_def_file_loc):

		control_file_sep_value = scenario.seperator_value(control_def_file_loc)
		control_file = scenario.control_file_values(control_file, control_file_sep_value)
		today = date.today()

		final_lines_to_file = {}

		text_file_summary_result = resultsfilelocation+"Summary_Result"+"/"+today_now+"/"+"summary_result.json"
		total_Summary_line = {}

		for i in range(0, len(datafiles_names)):
			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)
			client_file_data = pd.read_csv(client_file, sep= sep_value)
			json_def_data = pd.read_json(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]

			client_file_name_split = client_file_name[-len(client_file_name):-4]

			text_file_pass = resultsfilelocation+today_now+"/"+"Pass/"
			text_file_fail = resultsfilelocation+today_now+"/"+"Failed/"
			text_file_result = resultsfilelocation+today_now+"/"+"Result/"+client_file_name_split+".json"
			
			# row count validation

			# if int(control_file.xs(client_file_name)) != int(len(client_file_data)):
			# 	line1 = {"Test": "Rows count", "Result": "Failed", "Output": "The partner file has "+str(int(control_file.xs(client_file_name)))+" rows but control file has "+str(int(len(client_file_data)))}
			# else:
			# 	line1 = {"Test": "Rows count", "Result": "Passed"}

			#checking null values

			l4 = client_file_data
			dff = pd.DataFrame(l4)
			dff2=dff[dff.isnull().any(axis=1)]
			if(dff.isnull().sum().sum()):
				dff2.index=dff2.index+1
				output1= dff.columns[dff.isnull().any().tolist()] +":"+ str(dff2.index.tolist())
				line1 = {"Test name": "Check for nulls", "Result": "Failed/Nulls are found","Null values found in":output1.tolist()}
			else:
				line1 = {"Test name": "Check for nulls", "Result": "Passed"}

			# column names validation

			l1 = (list(client_file_data.columns))
			l2 = (list(json_def_data["columns"].index))

			if len(set(l1).intersection(l2)) == len(l2) :
				line2 = {"Test name": "Column names", "Result": "Passed"}
			else:
				line2 = {"Test name": "Column names", "Result": "Failed", "Output": "The partner file has other columns "+str(set(l1).union(l2) - set(l1).intersection(l2))}

			# column order validation

			l2 = (json_def_data["columns"])
			l2_values = (list(json_def_data["columns"].index))

			temp1 = []
			def_col, pass_list, fail_list = {}, {}, {}

			for index, col in enumerate(l2_values):
				if int(l2[col]['order']) <= len(l1):
					def_col[int(l2[col]['order'])-1] = col
					def_col.update(def_col)
			if len(def_col.keys()) != len(l1):
				fail_list[-1000] = "Length of the columns doesn't match and the columns present in partner files are"
				for i in range(len(l1)):
					fail_list[i] = str(l1[i])
			else:
				for i in def_col:
					if str(def_col[i]) == str(l1[i]):
						pass_list[i] = str(def_col[i])
					else:
						fail_list[i] = str(def_col[i])
			if len(fail_list) != 0:
				line3 = {"Test name": "Column order", "Result": "Failed", "Output": "The expected column order is "+str(list(def_col.values()))+" but we have "+str(list(fail_list.values()))}
			else:
				line3 = {"Test name": "Column order", "Result": "Passed"}

			# copying the file to passed or fail folder

			if line1["Result"] == "Passed" and line2["Result"] == "Passed" and line3["Result"] == "Passed":
				with open(text_file_pass+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
				Summary_line = {"FileName" : client_file_name, "TimeStamp" : today_now, "Result" : "Pass"}

			else:
				with open(text_file_fail+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
				Summary_line = {"FileName" : client_file_name, "TimeStamp" : today_now, "Result" : "Failed"}

			total_Summary_line[client_file_name] = Summary_line

			# writing the output to the result file

			final_lines_to_file = {"Test-1" : line1, "Test-2" : line2, "Test-3" : line3}

			# creating a json output file in result folder

			with open(text_file_result, "w") as output:
				json.dump(final_lines_to_file, output, indent=2)
			output.close()

		# writing to Summary result file

		with open(text_file_summary_result, 'a') as f2:
			json.dump(total_Summary_line, f2, indent=3)
		f2.close()

		return text_file_summary_result, final_lines_to_file
	