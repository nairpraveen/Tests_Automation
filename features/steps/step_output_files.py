from behave      import given, when, then
from hamcrest    import assert_that, equal_to
from files import retrieve_files
from file_comp import f_comp
from transformation import scenario
from dir_file import dir_create
from connect import connection


@given('a file')
def step_given_the_file(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
	context.files = retrieve_files()
	context.transformation = scenario()
	context.connect=connection()
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc, resultsfiles_loc)
	assert_that(len(datafiles_names) > 0)


@then('check null values')
def step_check_null_values(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
	datafiles_names, deffiles_names, control_data_file, control_def_file_loc = context.files.files(date, masterfile_loc, resultsfiles_loc)
	dir_file = dir_create()
	values = dir_file.dir(resultsfiles_loc)
	text_file_summary_result, final_lines_to_file = context.transformation.scenario_writing_to_files(values[0], resultsfiles_loc, datafiles_names, deffiles_names, control_data_file, control_def_file_loc)
	file_comp = f_comp()
	comparison = file_comp.comp(text_file_summary_result, resultsfiles_loc)


@then('column names should match')
def step_column_names_should_match(context):
	pass


@then('column order should match')
def step_column_order_should_match(context):
	pass


@then('empty rows')
def step_empty_rows(context):
	pass


@then('query result matched with partner file result')
def step_sql_test(context):
	pass	


@then('data type check')
def step_data_type_check(context):
	pass

@then ('special characters')
def step_special_characters(context):
	pass
