import pandas as pd
import glob, os, datetime
from dir_file import dir_create
from datetime import date
import json
from collections import OrderedDict
import os
import glob


class scenario(object):
    """docstring for Count"""

    def __init__(self):
        self.fn = None

    # def control_file_values(control_file, sep_value):

    # 	temp = pd.read_csv(control_file, sep='|')
    # 	df = pd.DataFrame()
    # 	df['NumberOfRows'] = temp['FileName'].apply(lambda x: x.split(sep_value)[1])
    # 	df['FileName'] = temp['FileName'].apply(lambda x: x.split(sep_value)[0])
    # 	df = df.groupby('FileName').sum()
    # 	return df


    def seperator_value(def_file_name):
        sep_value = pd.read_json(def_file_name)
        sep_value = sep_value.fieldseparator.ix[0]
        return sep_value

    def scenario_writing_to_files(self, resultsfilelocation, datafiles_names, deffiles_names, control_def_file_loc,date,timestamp):

        control_file_sep_value = scenario.seperator_value(control_def_file_loc)
        # control_file = scenario.control_file_values(control_file, control_file_sep_value)

        final_lines_to_file = {}
        pass_control_file_data, fail_control_file_data = [], []

        for i in range(0, len(datafiles_names)):
            client_file = datafiles_names[i]
            json_def = deffiles_names[i]
            sep_value = scenario.seperator_value(json_def)
            client_file_name = client_file.rsplit("/", 1)[1]
            json_def_name = json_def.split('/')[1]
            client_file_name_split = client_file_name[-len(client_file_name):-4]

            text_file_pass = resultsfilelocation + "/" + "Pass/"
            text_file_fail = resultsfilelocation + "/" + "Failed/"
            text_file_result = resultsfilelocation + "/" + "Result/" + client_file_name_split + ".json"
            pass_fail_control_file = resultsfilelocation + "/" + "Summary_Result/"

            client_file_data = pd.read_csv(client_file, sep=sep_value)
            json_def_data = json.load(open(json_def), object_pairs_hook=OrderedDict)

            l4 = client_file_data
            dff = pd.DataFrame(l4)
            dff2 = dff[dff.isnull().any(axis=1)]
            if (dff.isnull().sum().sum()):
                dff2.index = dff2.index + 1
                output1 = dff.columns[dff.isnull().any().tolist()] + ":" + str(dff2.index.tolist())
                line1 = {"Test name": "Check for nulls", "Result": "Failed/Nulls are found",
                         "Null values found in": output1.tolist()}
            else:
                line1 = {"Test name": "Check for nulls", "Result": "Passed"}

            # column names validation

            l1 = (list(client_file_data.columns))
            l2 = (list(json_def_data["columns"]))

            if len(set(l1).intersection(l2)) == len(l2):
                line2 = {"Test name": "Column names", "Result": "Passed"}
            else:
                line2 = {"Test name": "Column names", "Result": "Failed", "Output": {
                    "The partner file has other columns ":list(set(l1).union(l2) - set(l1).intersection(l2))}}

            # column order validation

            l3 = (json_def_data["columns"])
            temp1 = []
            def_col, pass_list, fail_list = {}, {}, {}

            for index, col in enumerate(l2):
                if int(l3[col]['order']) <= len(l1):
                    def_col[int(l3[col]['order']) - 1] = col
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

                line3 = {"Test name": "Column order", "Result": "Failed",
                         "Output": {"the expected column order is": list(def_col.values())},
                         "but the partner file has these columns with wrong order": list(fail_list.values())}

            else:
                line3 = {"Test name": "Column order", "Result": "Passed"}

            # copying the file to passed or fail folder

            if line1["Result"] == "Passed" and line2["Result"] == "Passed" and line3["Result"] == "Passed":
                with open(text_file_pass + client_file_name, 'w') as f1:
                    for line in open(client_file):
                        f1.write(line)
                Summary_line = {"FileName": client_file_name, "Result": "Pass"}

                # pass control file

                pass_control_file_data.append(client_file_name + "|" + str(len(client_file_data)))

            else:
                with open(text_file_fail + client_file_name, 'w') as f1:
                    for line in open(client_file):
                        f1.write(line)

                # failed control file

                fail_control_file_data.append(client_file_name)
                

            # writing the output to the result file

            final_lines_to_file = {"Test-1": line1, "Test-2": line2, "Test-3": line3}

            # creating a json output file in result folder

            with open(text_file_result, "w") as output:
                json.dump(final_lines_to_file, output, indent=4)
            output.close()

        pass_control_file='PassControl_'+date+"_"+timestamp+'.txt'
        with open(pass_fail_control_file+pass_control_file, 'w') as out:
            out.write('Filename|Rowcount')
            for line in pass_control_file_data:
            	out.write('\n'+line)

        if len(fail_control_file_data) != 0:
	        fail_file='FailedFile_'+date+"_"+timestamp+'.txt'
	        with open(pass_fail_control_file+fail_file,'w') as out2:
	            out2.write('Filename')
	            for line in fail_control_file_data:
	                out2.write('\n'+line)

        return final_lines_to_file