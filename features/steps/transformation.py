import pandas as pd
import glob, os, datetime
from dir_file import dir_create
from datetime import date

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


	def rows_count(self, datafiles_names, deffiles_names, control_file, control_def_file_loc):
		
		control_file_sep_value = scenario.seperator_value(control_def_file_loc)
		control_file = scenario.control_file_values(control_file, control_file_sep_value)
		today = date.today()
		rows_count_pass_list = []
		rows_count_fail_list = []

		for i in range(0, len(datafiles_names)):
			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)
			client_file_data = pd.read_csv(client_file, sep= sep_value)
			json_def_data = pd.read_json(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]
			if int(control_file.xs(client_file_name)) != int(len(client_file_data)):
				fail_list = "Rows count failed for " + client_file_name
				rows_count_fail_list.append(list(fail_list))
				text_file = "Result/Failed/"+str(today)+"/"+"rows_count"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(fail_list)
			else:
				# print("Rows count matched for {:s} file and count: {:d} \n".format( client_file_name ,int(control_file.xs(client_file_name))))
				pass_list = "Row count Passed for " + client_file_name
				rows_count_pass_list.append(list(pass_list))
				text_file = "Result/Pass/"+str(today)+"/"+"rows_count"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(pass_list)
				output.close()
		return rows_count_pass_list, rows_count_fail_list


	def column_names(self, datafiles_names, deffiles_names, control_file, control_def_file_loc):

		control_file_sep_value = scenario.seperator_value(control_def_file_loc)
		control_file = scenario.control_file_values(control_file, control_file_sep_value)
		today = date.today()
		column_names_pass_list = []
		column_names_fail_list = []

		for i in range(0, len(datafiles_names)):
			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)

			client_file_data = pd.read_csv(client_file, sep= sep_value)
			json_def_data = pd.read_json(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]
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
				pass_list = "Columns match Passed for "+client_file_name
				column_names_pass_list.append(list(pass_list))
				text_file = "Result/Pass/"+str(today)+"/"+"column_names"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(pass_list)
			else:
				# fail_list = fail_list.append(['These columns are not found in {:s} for {:s}'.format(json_def_name, client_file_name), list(set(l1) - set(l2))])
				fail_list = "Columns match failed for "+client_file_name
				column_names_fail_list.append(list(fail_list))
				text_file = "Result/Failed/"+str(today)+"/"+"column_names"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(fail_list)
		return column_names_pass_list, column_names_fail_list


	def column_order(self, datafiles_names, deffiles_names, control_file, control_def_file_loc):

		control_file_sep_value = scenario.seperator_value(control_def_file_loc)
		control_file = scenario.control_file_values(control_file, control_file_sep_value)
		today = date.today()
		column_order_pass_list = []
		column_order_fail_list = []

		for i in range(0, len(datafiles_names)):
			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)

			client_file_data = pd.read_csv(client_file, sep= sep_value)
			json_def_data = pd.read_json(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]
			l1 = (list(client_file_data.columns))
			l2 = (json_def_data['columns'])
			temp = []
			for index, col in enumerate(l1):
				try:
					if l2[col]['order'] == str(index+1):
						temp.append(col)
				except Exception as e:
					temp.append(col)
			# fail_list = fail_list.append(["Order is not match in {:s} for the following".format(json_def_name), temp])
			pass_order_list = []
			fail_order_list = []
			if l1[i] != temp[i]:
				pass_order_list.append(list("Not Equal"))
			else:
				for i in range(0, len(l1)):
					if l1[i] == temp[i]:
						pass_order_list.append(l1[i])
					else:
						fail_order_list.append(l1[i])
			if len(pass_order_list) == len(l1):
				pass_list = "Columns order Passed for "+client_file_name
				column_order_pass_list.append(list(pass_list))
				text_file = "Result/Pass/"+str(today)+"/"+"column_order"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(pass_list)
					output.write(str(pass_order_list))
			elif pass_order_list[0] == "Not Equal":
				fail_list = "Columns order failed for "+client_file_name
				column_order_fail_list.append(fail_list)
				text_file = "Result/Failed/"+str(today)+"/"+"column_order"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(fail_list)
					output.write(str(fail_order_list))
			else:
				fail_list = "Columns order failed for "+client_file_name
				column_order_fail_list.append(fail_list)
				text_file = "Result/Failed/"+str(today)+"/"+"column_order"+datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+"_"+client_file_name
				with open(text_file, "w") as output:
					output.write(fail_list)
					output.write(str(fail_order_list))
		return column_order_pass_list, column_order_fail_list
	