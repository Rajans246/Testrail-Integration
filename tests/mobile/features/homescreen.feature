@mobile
Feature: Raysil Home page

  Scenario: Verify details screen for selected product
    Given I am on Raysil application Home screen
    And I select Application and Range
    When I tap on Submit button
    Then I should see Details screen for Range
    And I tap Home Footer Icon