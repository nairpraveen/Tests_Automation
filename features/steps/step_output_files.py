from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from file_comp import f_comp
from transformation import scenario
from dir_file import dir_create


@given('a file')
def step_given_the_file(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	resultsfilelocation=context.config.userdata.get("resultsfilelocation")
	context.files = retrieve_files()
	context.transformation = scenario()
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc,resultsfilelocation)
	assert_that(len(datafiles_names) > 0)


@then('check null values')
def step_check_null_values(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	resultsfilelocation=context.config.userdata.get("resultsfilelocation")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc,resultsfilelocation)
	dir_file = dir_create()
	values = dir_file.dir(resultsfilelocation)
	text_file_summary_result, final_lines_to_file = context.transformation.scenario_writing_to_files(values[0],resultsfilelocation,datafiles_names, deffiles_names, control_data_file, control_def_file_loc)
	#print(text_file_summary_result)
	file_comp = f_comp()
	comparison = file_comp.comp(text_file_summary_result, resultsfilelocation)


@then('column names should match')
def step_column_names_should_match(context):
	pass


@then('column order should match')
def step_column_order_should_match(context):
	pass