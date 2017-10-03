from datetime import date
import pandas as pd
import glob, os, datetime, re
import json
import pypyodbc

from features.steps.connect import connection


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

		final_lines_to_file = {}

		text_file_summary_result = resultsfilelocation+"Summary_Result"+"/"+today_now+"/"+"summary_result.json"
		total_Summary_line = {}

		for i in range(0, len(datafiles_names)):

			client_file = datafiles_names[i]
			json_def = deffiles_names[i]
			sep_value = scenario.seperator_value(json_def)
			client_file_name = client_file.split('/')[2]
			json_def_name = json_def.split('/')[1]
			client_file_name_split = client_file_name[-len(client_file_name):-4]

			text_file_pass = resultsfilelocation+today_now+"/"+"Pass/"
			text_file_fail = resultsfilelocation+today_now+"/"+"Failed/"
			text_file_result = resultsfilelocation+today_now+"/"+"Result/"+client_file_name_split+".json"

			if client_file_name in list(control_file.index):

				client_file_data = pd.read_csv(client_file, sep= sep_value)
				json_def_data = pd.read_json(json_def)

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

				# checking the empty rows

				i = 1
				matches = {}
				empty_rows_list = []
				
				with open(client_file,'r') as out:
					for line in out:
						if line == '\n':
							matches[i] = "matched"
							matches.update(matches)
						else:
							matches[i] = "not matched"
							matches.update(matches)
						i = i +1

				key = list(matches.keys())
				val = list(matches.values())
				for i in range(len(val)):
					if val[i] == "matched":
						empty_rows_list.append("The file has empty row at "+str(key[i]))

				if len(empty_rows_list) != 0:
					line4 = {"Test name": "Empty Rows", "Result": "Failed", "Output": empty_rows_list}
				else:
					line4 = {"Test name": "Empty Rows", "Result": "Passed"}

				#aggregate_function check

				if(client_file_name=="test_20170504.csv"):

					def_agg_col = {}
					def_match={}
					data_match={}
					pass_list1=[]
					fail_list1=[]

					for index, col in enumerate(l2_values):
						def_agg_col[col] = l2[col]['aggregate_function']
						def_agg_col.update(def_agg_col)

					for index, col in enumerate(l2_values):
						query = l2[col]['sql_query']
						def_match[col]=connection.makeconnection(self, query)
						def_match.update(def_match)

					for col in client_file_data.columns:
						data_match[col]=len(client_file_data[col])
						data_match.update(data_match)

					for key in data_match.keys():
						if data_match[key]==def_match[key]:
							pass_list1.append("matched")
						else:
							fail_list1.append("not matched")
					if len(pass_list1)==len(data_match.keys()):
						line5={"Test name": "Summary Data check", "Result": "Passed"}
					else:
						line5={"Test name": "Summary Data check", "Result": "Failed"}
				else:
					line5={"Test name": "Summary Data check", "Result": "No aggregation function is defined for this file"}

				# check for the data-types

				data_file_columns = client_file_data.columns

				datatype_col = {}

				result_fail_list, column_pass_list, column_fail_list = [], [], []

				datatype_col_rename = {'INT' : 'int64', 'int' : 'int64', 'BIGINT' : 'int64', 'SMALLINT' : 'int64', 'NVARCHAR(50)' : 'str', 'CHAR(8)' : 'str', 'DECIMAL(18,2)' : 'float64' , 'BIT' : 'bool_',  'DECIMAL(18,4)' : 'float64', 'CHAR(2)' : 'str', 'VARCHAR(10)' : 'str', 'CHAR(1)' : 'str','VARCHAR(50)':'str', 'DATE' : 'date', 'NVARCHAR(3)' : 'str', 'NVARCHAR(500)' : 'str', 'NVARCHAR(100)' : 'str', 'NVARCHAR(255)' : 'str', 'nvarchar(255)' : 'str', 'NVARCHAR(25)' : 'str', 'NVARCHAR(3000)' : 'str', 'NVARCHAR(40)' : 'str', 'NVARCHAR(20)' : 'str'}

				for index, col in enumerate(l2_values):
					datatype_col[col] = l2[col]['dbtype']
					datatype_col.update(datatype_col)

				dict3 = {k:datatype_col_rename[v] for k,v in datatype_col.items()}
				for column in data_file_columns:
					if column in dict3.keys():
						for val in client_file_data[column]:
							if str(val) == "nan" or type(val).__name__ == dict3[column]:
								column_pass_list.append(column)
							else:
								column_fail_list.append(column)
								result_fail_list.append("the value "+ str(val) + " at row "+ str(i) + " in column "+str(column)+" doesn't match with datatype "+datatype_col[column])
							i = i + 1

				if len(set(column_pass_list)) == len(dict3.keys()):
					line6 = {"Test name": "Data type", "Result": "Passed"}
				elif len(client_file_data) == 0:
					line6 = {"Test name": "Data type", "Result": "Failed", "Output": "File doesn't have any data"}
				else:
					line6 = {"Test name": "Data type", "Result": "Failed", "Output": result_fail_list}

				# copying the file to passed or fail folder

				if line1["Result"] == "Passed" and line2["Result"] == "Passed" and line3["Result"] == "Passed" and line4["Result"] == "Passed" and line5["Result"] == "Passed" and line6["Result"] == "Passed":
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

				final_lines_to_file = {"Test-1" : line1, "Test-2" : line2, "Test-3" : line3, "Test-4" : line4, "Test-5" : line5, "Test-6" : line6}

				# creating a json output file in result folder

				with open(text_file_result, "w") as output:
					json.dump(final_lines_to_file, output, indent=2)
				output.close()

			else:

				total_Summary_line[client_file_name] = {"FileName" : client_file_name, "TimeStamp" : today_now, "Result" : "File doesn't exist in the control file"}

		# writing to Summary result file

		with open(text_file_summary_result, 'a') as f2:
			json.dump(total_Summary_line, f2, indent=3)
		f2.close()

		return text_file_summary_result, final_lines_to_file
	
