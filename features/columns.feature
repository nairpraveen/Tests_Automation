
Feature: Check whether the columns exists or not

@all
Scenario: Proper columns present
   Given  the file
    Then  rows count should match

@all
Scenario: Row counts match control file
   Given  the file
    Then  column names should match

@all
Scenario: Row counts match control file
   Given  the file
    Then  column order should match
