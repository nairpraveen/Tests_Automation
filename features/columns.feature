
Feature: To check whether the columns exists,column names match,column order match and compare the row counts.

@all
Scenario: To check if the number of rows given in the control file match with the definition file.
   Given  a file
    Then  row count should match

@all
Scenario: To check if the column names in partner file and definition file match.
   Given  a file
    Then  column names should match

@all
Scenario: To check if the order of the column names match in partner file and definition file.
   Given  a file
    Then  column order should match

@all
Scenario: Check for null values
  Given   a file
  Then    null values are not allowed
