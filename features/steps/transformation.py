import pandas as pd
import glob, os, datetime
from dir_file import dir_create
from datetime import date
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
		sep_value = sep_value.feildseperator.ix[0]
		return sep_value


	def scenario_writing_to_files(self, datafiles_names, deffiles_names, control_file, control_def_file_loc):

		control_file_sep_value = scenario.seperator_value(control_def_file_loc)
		control_file = scenario.control_file_values(control_file, control_file_sep_value)
		today = date.today()

		final_lines_to_file = {}

		for i in range(0, len(datafiles_names)):
			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)
			client_file_data = pd.read_csv(client_file, sep= sep_value)
			json_def_data = pd.read_json(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]

			client_file_name_split = client_file_name[-len(client_file_name):-4]

			text_file_pass = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+"/"+"Pass/"
			text_file_fail = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+"/"+"Failed/"
			text_file_result = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')+"/"+"Result/"+client_file_name_split+".json"

			if int(control_file.xs(client_file_name)) != int(len(client_file_data)):
				line1 = {"Key": "Rows count", "Result": "Failed", "Output": "The partner file has "+str(int(control_file.xs(client_file_name)))+" rows but definition file has "+str(int(len(client_file_data)))}
				with open(text_file_fail+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
			else:
				line1 = {"Key": "Rows count", "Result": "Passed"}
				with open(text_file_pass+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)


			l1 = (list(client_file_data.columns))
			l2 = (json_def_data["columns"])
			temp = []
			for index, col in enumerate(l1):
				try:
					if l2[col]['order'] == str(index+1):
						temp.append(col)
				except Exception as e:
					temp.append(col)
			if l1 == temp :
				line2 = {"Key": "Column names", "Result": "Passed"}
				with open(text_file_pass+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
			else:
				line2 = {"Key": "Column names", "Result": "Failed", "Output": "The partner file has "+str(l1)+" columns but definition file has "+str(temp)}
				with open(text_file_fail+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)


			temp1 = []
			for index, col in enumerate(l1):
				try:
					if l2[col]['order'] == str(index+1):
						temp1.append(col)
				except Exception as e:
					temp1.append(col)
			pass_order_list = []
			fail_order_list = []
			if l1[i] != temp1[i]:
				pass_order_list.append(list("Not Equal"))
			else:
				for i in range(0, len(l1)):
					if l1[i] == temp1[i]:
						pass_order_list.append(l1[i])
					else:
						fail_order_list.append(l1[i])
			if len(pass_order_list) == len(l1):
				line3 = {"Key": "Column order", "Result": "Passed"}
				with open(text_file_pass+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
			elif pass_order_list[0] == "Not Equal":
				line3 = {"Key": "Column order", "Result": "Failed"}
				with open(text_file_fail+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
			else:
				line3 = {"Key": "Column order", "Result": "Failed"}
				with open(text_file_fail+client_file_name, 'w') as f1:
					for line in open(client_file):
						f1.write(line)
			final_lines_to_file = {"Scenario1":line1, "Scenario2":line2, "Scenario3":line3}
			with open(text_file_result, "w") as output:
				json.dump(final_lines_to_file, output)
			output.close()

		return final_lines_to_file
	