
Feature: To check the null values,column names match,column order match.

@all
Scenario: To check if there are any null values
   Given  a file
    Then  check null values

@all
Scenario: To check if the column names in partner file and definition file match
   Given  a file
    Then  column names should match

@all
Scenario: To check if the order of the column names match in partner file and definition file
   Given  a file
    Then  column order should match