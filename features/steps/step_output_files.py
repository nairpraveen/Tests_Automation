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
	resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
	timestamp = context.config.userdata.get("timestamp")
	context.files = retrieve_files()
	context.transformation = scenario()


@then('check null values')
def step_check_null_values(context):
	date = context.config.userdata.get("date")
	masterfile_loc = context.config.userdata.get("masterfile_loc")
	resultsfiles_loc = context.config.userdata.get("resultsfiles_loc")
	timestamp = context.config.userdata.get("timestamp")
	datafiles_names, deffiles_names, control_def_file_loc = context.files.files(date, masterfile_loc, resultsfiles_loc, timestamp)
	dir_file = dir_create()
	values = dir_file.dir(resultsfiles_loc)
	text_file_summary_result, final_lines_to_file = context.transformation.scenario_writing_to_files( resultsfiles_loc, datafiles_names, deffiles_names, control_def_file_loc)
	file_comp = f_comp()
	comparison = file_comp.comp(text_file_summary_result, datafiles_names, date, timestamp, resultsfiles_loc)


@then('column names should match')
def step_column_names_should_match(context):
	pass


@then('column order should match')
def step_column_order_should_match(context):
	pass